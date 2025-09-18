from Lesson_07.task_additional.task_add_02_send_manager import \
	message_dispatcher, message_sender, services

if __name__ == "__main__":
	sms_service = services.SMSService()
	email_service = services.EmailService()
	push_service = services.PushService()
	
	sms_sender = message_sender.SMSAdapter(sms_service,
	                                       "+380501234567")
	email_sender = message_sender.EmailAdapter(email_service,
	                                           "user@example.com")
	push_sender = message_sender.PushAdapter(push_service,
	                                         "device2025")
	
	for sender in [sms_sender, email_sender, push_sender]:
		sender.send_message("Your confirmation code: 200")
	
	print()
	dispatcher = message_dispatcher.MessageDispatcher([sms_sender,
	                                                   email_sender,
	                                                   push_sender])
	
	dispatcher.dispatch("Your confirmation code: 300")
