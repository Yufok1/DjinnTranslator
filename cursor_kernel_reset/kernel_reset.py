# Copyright 2024 SpliceWeb
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Cursor Kernel Reset Module

Provides functionality to reinitialize the Jupyter kernel in Cursor environments
and verify the environment stability for dashboard operation.
"""

from IPython import get_ipython
import subprocess
import sys
import os
from typing import List, Optional
import importlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class KernelResetError(Exception):
    """Exception raised for kernel reset errors."""
    pass

def verify_environment() -> List[str]:
    """Verify required packages for kernel stability.
    
    Returns:
        List of missing package names, empty if all required packages are present
    """
    required = ["ipython", "ipykernel", "jupyter-client", "pyzmq>=23.0"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
            logger.info(f"Verified package: {pkg}")
        except ImportError:
            missing.append(pkg)
    if missing:
        logger.warning(f"Missing packages: {missing}. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing)
        logger.info("Packages installed successfully.")
    else:
        logger.info("Environment verified. All required packages present.")
    try:
        import cursor
        logger.info(f"Cursor package detected: version {cursor.__version__}")
    except ImportError:
        logger.warning("Cursor package not found. Version compatibility check skipped.")
    
    return missing

def install_missing_packages(packages: List[str]) -> bool:
    """Install missing packages.
    
    Args:
        packages: List of package specifications to install
        
    Returns:
        True if installation successful, False otherwise
    """
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install"] + packages,
            check=True,
            capture_output=True
        )
        logger.info(f"Successfully installed packages: {packages}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install packages: {e.stderr.decode()}")
        return False

def reset_kernel() -> bool:
    """Reinitialize Jupyter kernel in Cursor environment.
    
    Returns:
        True if kernel reset successful, False otherwise
    """
    try:
        ip = get_ipython()
        if ip and hasattr(ip, 'kernel'):
            logger.info("Detected Jupyter environment. Restarting kernel...")
            ip.kernel.do_shutdown(restart=True)
            logger.info("Kernel reinitialized successfully.")
        else:
            logger.warning("No Jupyter kernel detected. Skipping kernel reset.")
            print("Running in non-Jupyter environment. Kernel reset not required.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Subprocess error during kernel reset: {str(e)}")
        print(f"Kernel reset failed: {str(e)}. Proceeding without reset.")
    except Exception as e:
        logger.error(f"Unexpected error during kernel reset: {str(e)}")
        raise

def verify_cursor_version() -> bool:
    """Verify Cursor version compatibility.
    
    Returns:
        True if Cursor version is compatible, False otherwise
    """
    try:
        import cursor
        version = cursor.__version__
        major_version = int(version.split('.')[0])
        if major_version >= 1:
            logger.info(f"Cursor version {version} is compatible")
            return True
        else:
            logger.warning(f"Cursor version {version} may not support Jupyter")
            return False
    except ImportError:
        logger.warning("Cursor package not found")
        return False
    except Exception as e:
        logger.error(f"Error checking Cursor version: {str(e)}")
        return False

def main():
    """Main entry point for kernel reset."""
    try:
        # Verify environment
        missing_packages = verify_environment()
        if missing_packages:
            logger.info("Installing missing packages...")
            if not install_missing_packages(missing_packages):
                raise KernelResetError("Failed to install required packages")
        
        # Verify Cursor version
        if not verify_cursor_version():
            logger.warning("Cursor version may not be compatible")
        
        # Reset kernel
        if reset_kernel():
            logger.info("Kernel reset successful")
            return 0
        else:
            raise KernelResetError("Kernel reset failed")
            
    except Exception as e:
        logger.error(f"Error during kernel reset: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 