import os
import logging
from typing import Optional
from abc import ABC, abstractmethod

class AbstractScriptManager(ABC):
    log = logging.getLogger("AbstractScriptManager")

    def __init__(self):
        self.engine = None

    def get_invocable(self, path: str, client: Optional['MapleClient']) -> Optional[callable]:
        """
        Load and return an invocable script (e.g., a function or class) by path.
        """
        try:
            path = os.path.join("scripts", path)
            self.engine = None

            if client is not None:
                self.engine = client.get_script_engine(path)
            
            if self.engine is None:
                if not os.path.exists(path):
                    return None

                with open(path, "r") as file:
                    code = file.read()
                    exec_namespace = {}
                    exec(code, exec_namespace)
                    self.engine = exec_namespace  
                
                if client is not None:
                    client.set_script_engine(path, self.engine)
            
            return self.engine.get("main") if "main" in self.engine else None
        
        except Exception as e:
            self.log.error("Error executing script: %s", e)
            return None

    def reset_context(self, path: str, client: 'MapleClient'):
        """
        Reset or clear the script engine for the given path in the client.
        """
        path = os.path.join("scripts", path)
        client.remove_script_engine(path)
