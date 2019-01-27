from abc import ABC, abstractmethod


class Configuration(ABC):
	def __init__(self):
		self._file_name = 'Nothing'
	
	@property
	@abstractmethod
	def file_name(self):
		return self._file_name
	

class DevConfiguration(Configuration):
	@property
	def file_name(self):
		return 'self._file_name'
	

class ProdConfiguration(Configuration):
	@property
	def file_name(self):
		return 'ProdConfiguration'

class ConfigurationFactory():
	def __init__(self, production = True):
		self._configuration: Configuration = None
		if production:
			self._configuration = ProdConfiguration()
		else:
			self._configuration = DevConfiguration()
	
	@property
	def configuration(self) -> Configuration:
		return self._configuration


configuration_factory: ConfigurationFactory = ConfigurationFactory(False)

print(configuration_factory.configuration.file_name)
	