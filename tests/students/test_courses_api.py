import pytest as pytest
from rest_framework.test import APIClient
from students.models import Student, Course
from model_bakery import baker

@pytest.fixture
def client():
    return APIClient()
#
@pytest.fixture
def user():
    return Student.objects.create_user('STUDENT-admin')
#
@pytest.mark.django_db
def test_answer_me(client):
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200

BASE_URL = '/api/v1/courses/'

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

# проверка получения 1го курса
@pytest.mark.django_db
def test_get_course(client, course_factory, student_factory):

    students = student_factory(_quantity=5)
    courses = course_factory(_quantity=2, students=students)
    print(courses)
    url = BASE_URL + str(courses[0].id) + '/'
    response = client.get(url)
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == courses[0].id

# проверка получения списка курсов
@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(BASE_URL)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, d in enumerate(data):
        assert d['id'] == courses[i].id

# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_get_course_filter_id(client, course_factory):
    courses = course_factory(_quantity=2)
    url = BASE_URL + '?id=' + str(courses[0].id)
    response = client.get(url)
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == courses[0].id

# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_get_course_filter_name(client, course_factory):
    courses = course_factory(_quantity=10)
    url = BASE_URL + '?name=' + courses[0].name
    response = client.get(url)
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == courses[0].name

# тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post(BASE_URL, data={'name': 'Курс_1'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=10)
    url = BASE_URL + str(courses[0].id) + '/'
    response = client.patch(url, data={'name': 'Курс_2'})
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == 'Курс_2'

# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=10)
    count = Course.objects.count()
    url = BASE_URL + str(courses[0].id) + '/'
    response = client.delete(url)
    assert response.status_code == 204
    assert Course.objects.count() == count - 1