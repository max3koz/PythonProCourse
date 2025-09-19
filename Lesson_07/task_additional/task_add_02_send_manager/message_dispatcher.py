from typing import List

from Lesson_07.task_additional.task_add_02_send_manager.message_sender import \
	MessageSender


class MessageDispatcher:
	"""
	Class for sending messages via a list of adapters.
	Handles errors for each channel separately.
	"""
	
	def __init__(self, senders: List[MessageSender]) -> None:
		self.senders = senders
	
	def dispatch(self, message: str) -> None:
		"""
		Sends messages through all adapters in the list with error handling
		on individual adapters.
		"""
		for sender in self.senders:
			try:
				sender.send_message(message)
			except Exception as e:
				sender_name = sender.__class__.__name__
				print(f"Error in {sender_name}: {e}")
