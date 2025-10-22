from datetime import date
from typing import Any, Dict

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


def home(request: HttpRequest) -> HttpResponse:
	"""Home page with welcome text."""
	return render(request, 'main/home.html')


def about(request: HttpRequest) -> HttpResponse:
	"""'About us' page with information about the company."""
	context: Dict[str, Any] = {
		'company_description': "Наша компанія надає послуги з навчання "
		                       "інформатиці, математиці та робототехниці...",
		'last_updated': date.today(),
	}
	return render(request, 'main/about.html', context)


class ContactView(TemplateView):
	"""The class to display of the contact page."""
	template_name = 'main/contact.html'
	
	def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
		context = super().get_context_data(**kwargs)
		context.update({
			# commented out to check the defaut value in contact.html
			# 'address': 'New address, 123',
			'phone': '+380 99 123 4567',
			'email': 'sample@example.com',
			'work_time': '<strong>Ми працюємо щодня з 12:00 до 22:00.</strong>',
		})
		return context


class ServiceView(TemplateView):
	"""The class to display list of services"""
	template_name = 'main/services.html'
	
	def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
		context = super().get_context_data(**kwargs)
		all_services = [
			{'name': 'Заняття з математики',
			 'description': 'Підтягування знань за предметом, підготовка '
			                'до здачі екзаменів'},
			{'name': 'Заняття з програмування',
			 'description': 'Навчання програмуванню у Skretch, Python, C++ '
			                'від 5 років і до несхочу'},
			{'name': 'Заняття з програмування контролерів',
			 'description': 'Навчання програмуванню контролерів Microbit та '
			                'Arduino зі Skretch'},
			{'name': 'Заняття з Лего роботики',
			 'description': 'Заняття з робототехніки з наборами Lego Education'},
			{'name': 'Послуга 5',
			 'description': 'Немає інформації по послузі 5'},
			{'name': 'Послуга 6',
			 'description': 'Немає інформації по послузі 6'},
		]
		
		query = self.request.GET.get('q', '').lower()
		if query:
			filtered = [s for s in all_services
			            if query in s['name'].lower() or query in s[
				            'description'].lower()
			            ]
			context['services'] = filtered
		else:
			context['services'] = all_services
		
		context['last_updated'] = date.today()
		context['has_contacts'] = True
		return context
