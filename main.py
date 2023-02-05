import time
import json
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt

results = []
for page_n in range(1, 64):
    url = requests.get(f'https://qyzmet.kz/vacansii?page={page_n}').text
    soup = BeautifulSoup(url, 'html.parser')
    jobs = soup.find_all('article', class_='job no-logo')
    for job in jobs:
        job_name = ' '.join(job.find('h2', class_="title").text.split())
        company_name = ' '.join(job.find('div', class_="job-data company").text.split())
        city = ''.join(job.find('div', class_='job-data region').text.split())
        salary_container = job.find('div', class_='job-data salary')
        descContainer = ' '.join(job.find('div', class_='desc').text.split())
        if salary_container:
            salary = ''.join(salary_container.text.replace('От', '', ).replace('KZT', '')
                             .replace('До', '', ).replace('₸', '', ).split())
            if "RUB" in salary and "-" not in salary:
                salary = int(salary.replace("RUB", "").replace(",", "")) * 6
                salary = str(salary)
            elif '.' in salary:
                salary = int(salary.replace(".", "").replace(",", "")).split()
                salary = str(salary)
            elif "$" in salary and "-" not in salary:
                salary = int(salary.replace("$", "").replace(",", "")) * 480
                salary = str(salary)
            elif "€" in salary and "-" not in salary:
                salary = int(salary.replace("€", "").replace(",", "")) * 500
                salary = str(salary)
            elif '-' and 'RUB' in salary:
                salary_range = salary.replace("RUB", "").replace(",", "").split("-")
                lower_salary = int(salary_range[0])
                upper_salary = int(salary_range[1])
                salary = str(int((lower_salary + upper_salary) / 2 * 6))
            elif '-' and '$' in salary:
                salary_range = salary.replace("$", "").replace(",", "").split("-")
                lower_salary = int(salary_range[0])
                upper_salary = int(salary_range[1])
                salary = str(int((lower_salary + upper_salary) / 2 * 480))
            elif '-' and '€' in salary:
                salary_range = salary.replace("€", "").replace(",", "").split("-")
                lower_salary = int(salary_range[0])
                upper_salary = int(salary_range[1])
                salary = str(int((lower_salary + upper_salary) / 2 * 500))
            elif "-" in salary:
                salary_range = salary.split("-")
                avg_salary = (int(salary_range[0].replace(",", "")) + int(salary_range[1].replace(",", ""))) / 2
                salary = str(int(avg_salary))
            else:
                salary = int(salary.replace(",", ""))
                salary = str(salary)
        else:
            salary = None

        if descContainer:
            desc = ' '.join(job.find('div', class_='desc').text.split())
        else:
            desc = 'No Description'

        result = {
            'Job': job_name,
            'Company_Name': company_name,
            'City': city,
            'Salary': salary,
            'Description': desc
        }
        results.append(result)
    print(page_n)
    time.sleep(1)

# Plotting the distribution of salaries
salaries = [result['Salary'] for result in results if result['Salary']]
salaries = [float(salary.replace(',', '')) for salary in salaries]
salaries = [int(round(salary)) for salary in salaries]

plt.hist(salaries, bins=20)
plt.xlabel('Salary')
plt.ylabel('Frequency')
plt.title('Distribution of Salaries')
plt.show()



# Plotting the number of jobs by city
from collections import Counter

city_count = Counter([result['City'] for result in results])

fig = plt.figure(figsize=(20,10)) # increase the figure size
plt.bar(city_count.keys(), city_count.values())
plt.xlabel('City')
plt.ylabel('Number of Jobs')
plt.title('Number of Jobs by City')
plt.xticks(rotation=90)
plt.show()


with open('qyzmet.json.', 'w') as outfile:
    json.dump(results, outfile)