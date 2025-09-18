class SMSService:
	def send_sms(self, phone_number: str, message: str) -> None:
		print(f"Send SMS to {phone_number}: {message}")


class EmailService:
	def send_email(self, email_address: str, message: str) -> None:
		print(f"Send Email to {email_address}: {message}")


class PushService:
	def send_push(self, device_id: str, message: str) -> None:
		print(f"Push message to device {device_id}: {message}")
