from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestConversationsList(APITestCase):
    USERNAME = "test_user"
    PASSWORD = "123"

    TITLE = "test_title"

    URL = "/api/v1/conversations/"

    LOGIN_URL = "/api/v1/users/login/"

    def setUp(self):
        # user 생성
        user = User.objects.create(
            username=self.USERNAME,
        )
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user

        # conversation 생성
        conversation = models.Conversation.objects.create(
            owner=self.user,
            title=self.TITLE,
        )
        conversation.save()
        self.conversation = conversation

        # token 얻기
        response = self.client.post(
            self.LOGIN_URL,
            data={
                "username": self.USERNAME,
                "password": self.PASSWORD,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        token = response.json()["token"]
        self.token = token

    def test_get_conversation(self):

        # 로그인하지 않고 get 해보기
        response = self.client.get(self.URL)
        self.assertEqual(
            response.status_code,
            403,
        )

        # 로그인하고 get 해보기
        response = self.client.get(
            self.URL,
            headers={
                "jwt": self.token,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()
        # print(data)
        # [{'id': 1, 'owner': 'test_user', 'created_at': '2024-10-20T05:24:07.427105Z', 'updated_at': '2024-10-20T05:24:07.427260Z', 'title': 'test_title'}]

        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["id"],
            1,
        )
        self.assertEqual(
            data[0]["owner"],
            self.USERNAME,
        )
        self.assertEqual(
            data[0]["title"],
            self.TITLE,
        )
        self.assertIn(
            "created_at",
            data[0],
        )
        self.assertIn(
            "updated_at",
            data[0],
        )

    def test_post_conversation(self):

        # 로그인하지 않고 post 하는 경우
        response = self.client.post(self.URL)
        self.assertEqual(
            response.status_code,
            403,
        )

        # 여기서부터 로그인하고 테스트 진행
        # 로그인 후 아무 데이터 없이 post
        response = self.client.post(
            self.URL,
            headers={
                "jwt": self.token,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )

        # title 넘겨서 post
        test_title = "test_title_post"
        response = self.client.post(
            self.URL,
            data={
                "title": test_title,
            },
            headers={
                "jwt": self.token,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()
        # print(data)
        # {'id': 2, 'owner': {'username': 'test_user', 'email': ''}, 'created_at': '2024-10-20T05:13:11.440107Z', 'updated_at': '2024-10-20T05:13:11.440119Z', 'title': 'test_title'}

        self.assertEqual(
            data["id"],
            2,
        )
        self.assertEqual(
            data["owner"]["username"],
            self.USERNAME,
        )
        self.assertEqual(
            data["owner"]["email"],
            "",
        )
        self.assertEqual(
            data["title"],
            test_title,
        )
        self.assertIn(
            "created_at",
            data,
        )
        self.assertIn(
            "updated_at",
            data,
        )