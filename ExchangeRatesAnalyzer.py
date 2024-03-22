import requests
from datetime import datetime, timedelta
import json

class ExchangeRatesAnalyzer:
    def __init__(self, base_currency='AUD', target_currency='NZD'):
        """
        Initializes the ExchangeRatesAnalyzer object with base and target currencies,
        and constructs the API URL.
        """
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.api_url = f'https://api.exchangerate-api.com/v4/latest/{base_currency}'
        
    def fetch_exchange_rates(self, date):
        """
        Fetches exchange rates from the API for a specific date.

        :param date: The date for which exchange rates are fetched.
        :return: Exchange rate for the specified date and target currency.
        """
        response = requests.get(f'{self.api_url}?date={date.strftime("%Y-%m-%d")}')
        response.raise_for_status()
        return response.json()['rates'][self.target_currency]
    
    def analyze_and_output(self):
        """
        Analyzes exchange rates for the past 30 days and generates output in JSON format.

        :return: JSON-formatted output containing exchange rates data and statistics.
        """
        # Get today's date
        today = datetime.now()
        # Generate a list of dates for the past 30 days
        past_30_days = [today - timedelta(days=i) for i in range(30)]
        
        # Fetch exchange rates for each date in the past 30 days
        rates = [{'Date': date.strftime('%Y-%m-%d'), 'Exchange rate': self.fetch_exchange_rates(date)} for date in past_30_days]
        
        # Calculate statistics
        best_rate = max(rates, key=lambda x: x['Exchange rate'])
        worst_rate = min(rates, key=lambda x: x['Exchange rate'])
        average_rate = round(sum(rate['Exchange rate'] for rate in rates) / len(rates), 4)

        # Construct output JSON
        output = {
            'exchange_rates': rates,
            'statistics': {
                'best_rate': best_rate,
                'worst_rate': worst_rate,
                'average_rate': average_rate
            }
        }
        return json.dumps(output, indent=4)

if __name__ == "__main__":
    # Create an instance of ExchangeRatesAnalyzer
    analyzer = ExchangeRatesAnalyzer()
    # Perform analysis and output results
    output_json = analyzer.analyze_and_output()
    print(output_json)