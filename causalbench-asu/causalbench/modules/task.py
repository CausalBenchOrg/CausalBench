import os
from abc import ABC, abstractmethod
from importlib.util import spec_from_file_location, module_from_spec

from bunch_py3 import Bunch

from causalbench.commons.utils import package_module
from causalbench.modules.module import Module
from causalbench.services.requests import save_module, fetch_module


class AbstractTask(ABC):

    @abstractmethod
    def helpers(self) -> any:
        raise NotImplementedError

    @abstractmethod
    def model_data_inputs(self) -> dict[str, type]:
        raise NotImplementedError

    @abstractmethod
    def metric_data_inputs(self) -> dict[str, type]:
        raise NotImplementedError

    @abstractmethod
    def metric_model_inputs(self) -> dict[str, type]:
        raise NotImplementedError


class Task(Module):

    def __init__(self, module_id: int = None, version: int = None, zip_file: str = None):
        super().__init__(module_id, version, zip_file)

    def instantiate(self, arguments: Bunch):
        # TODO: Create the structure of the new instance
        pass

    def validate(self):
        # TODO: Perform logical validation of the structure
        pass

    def fetch(self):
        return fetch_module(self.type,
                            self.module_id,
                            self.version,
                            'tasks',
                            'downloaded_task.zip')

    def save(self, state, public: bool) -> bool:
        zip_file = package_module(state, self.package_path)
        self.module_id, self.version = save_module(self.type,
                                                   self.module_id,
                                                   self.version,
                                                   public,
                                                   zip_file,
                                                   'tasks',
                                                   'task.zip')
        return self.module_id is not None

    def load(self) -> AbstractTask:
        # form the proper file path
        file_path = os.path.join(self.package_path, self.path)

        # load the module
        spec = spec_from_file_location('module', file_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        # create an instance of the task
        class_name = getattr(module, self.class_name)
        task: AbstractTask = class_name()

        return task
