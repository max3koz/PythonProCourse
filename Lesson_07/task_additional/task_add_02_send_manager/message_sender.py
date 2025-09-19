from Lesson_07.task_additional.task_add_02_send_manager.services import \
	SMSService, EmailService, PushService


class MessageSender:
	"""The universal interface for sending messages."""
	
	def send_message(self, message: str) -> None:
		pass


class SMSAdapter(MessageSender):
	def __init__(self, service: SMSService, phone_number: str) -> None:
		self.service = service
		self.phone_number = phone_number
	
	def send_message(self, message: str) -> None:
		self.service.send_sms(self.phone_number, message)


class EmailAdapter(MessageSender):
	def __init__(self, service: EmailService, email_address: str) -> None:
		self.service = service
		self.email_address = email_address
	
	def send_message(self, message: str) -> None:
		self.service.send_email(self.email_address, message)


class PushAdapter(MessageSender):
	def __init__(self, service: PushService, device_id: str) -> None:
		self.service = service
		self.device_id = device_id
	
	def send_message(self, message: str) -> None:
		self.service.send_push(self.device_id, message)
