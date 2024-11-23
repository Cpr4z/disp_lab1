import requests

BASE_URL = 'http://51.250.46.215:8080/api/v1/persons/'

def get_persons(person_id = -1):
    msg = ''
    if person_id == -1:
        response = requests.get(BASE_URL)
    else:
        msg = f'{person_id}'
        response = requests.get(f'{BASE_URL}{person_id}/')
    if response.status_code == 200:
        print(f'GET: Person for ID ' + msg + ': ', response.json())
    elif response.status_code == 404:
        print(f'GET: Person for ID ' + msg + 'not found', response.json())
    else:
        print(f'GET: Unknown Error: {response.status_code}')

def create_persons(name, age, address, work):
    response = requests.post(BASE_URL, json={'name': name, 'age': age, 'address': address, 'work': work})
    if response.status_code == 201:
        print(f'POST: Created new Person ' + name + ': ', response.json())
    elif response.status_code == 400:
        try:
            print(f'POST: Invalid data: ', response.json())
        except ValueError:
            print(f'POST: Response is not JSON format: ', response.json())
    print('POST:', response.json())

def update_persons(person_id, name, age, address, work):
    url = f'{BASE_URL}{person_id}/'
    data = {'name': name, 'age': age, 'address': address, 'work': work}
    response = requests.patch(url, json=data)
    if response.status_code == 200:
        print(f'PATCH: Person for ID {person_id} was updated: ', response.json())
    elif response.status_code == 400:
        print(f'PATCH: Invalid data: ', response.json())
    elif response.status_code == 404:
        print(f'PATCH: Not found Person for ID {person_id}: ')
    else:
        print(f'PATCH: Error: {response.status_code}', response.text)



def delete_persons(person_id):
    response = requests.delete(f'{BASE_URL}{person_id}/')

    if response.status_code == 204:
        print(f'Item with id {person_id} successfully deleted.')
    else:
        print(f'Failed to delete item. Status code: {response.status_code}')
        try:
            print('Response:', response.json())
        except ValueError:
            print('Response is not in JSON format:', response.text)


if __name__ == '__main__':
    # Примеры использования клиента
    create_persons('Matvey', 24, 'Kuzminki', 'Engineer')
    create_persons('Artem', 19, 'Baumanskaya', 'Programmer')
    get_persons(1)
    update_persons(2, 'name', 12, 'address', 'work')  # замените 1 на нужный id
    get_persons(2)
    delete_persons(2)  # замените 1 на нужный id
    get_persons()