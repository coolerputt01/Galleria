from django.test import TestCase
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from .models import Album, Photo, Likes, PhotoView

def make_test_image(name="test.jpg", size=(10,10), color=(255,0,0)):
    img = Image.new("RGB", size, color)
    byte_io = BytesIO()
    img.save(byte_io, format="JPEG")
    byte_io.seek(0)
    return SimpleUploadedFile(name, byte_io.read(), content_type="image/jpeg")

User = get_user_model()

class AlbumTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(
            email="olumideadekolu9@gmail.com",
            display_name="coolerputt001",
            bio="Thank you LORD"
        )

    def test_album_creation(self):
        album = Album.objects.create(
            user=self.user,
            album_name="Album 1",
            album_desc="Some info"
        )
        self.assertIsNotNone(album)
        self.assertEqual(album.user, self.user)
        self.assertEqual(album.album_name, "Album 1")
        self.assertTrue(album.is_public)
        self.assertFalse(album.is_pinned)

    def test_album_pinning_limit(self):
        # Pin 5 albums
        for i in range(5):
            Album.objects.create(
                user=self.user,
                album_name=f"Pinned Album {i+1}",
                is_pinned=True
            )
        # Try to pin a 6th album, should raise ValueError
        with self.assertRaises(ValueError):
            Album.objects.create(user=self.user, album_name="Too Many", is_pinned=True)

class PhotoTestCase(TestCase):
    def setUp(self):
        self.test_image = make_test_image();
        self.user = User.objects.create(
            email="olumideadekolu9@gmail.com",
            display_name="coolerputt001",
            bio="Thank you LORD"
        )
        self.album = Album.objects.create(user=self.user, album_name="Album 1")
        
    def test_photo_creation(self):
        photo = Photo.objects.create(
            album=self.album,
            photo_name="Photo 1",
            photo_desc="Some photo info",
            photo_img=self.test_image
        )
        self.assertIsNotNone(photo)
        self.assertEqual(photo.album, self.album)
        self.assertEqual(photo.photo_name, "Photo 1")
        self.assertTrue(photo.resolution)  # Should be set after save

class LikesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@example.com", display_name="coolerputt002")
        self.album = Album.objects.create(user=self.user, album_name="Album 1")

    def test_like_creation(self):
        like = Likes.objects.create(user=self.user, album=self.album)
        self.assertIsNotNone(like)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.album, self.album)

    def test_like_unique(self):
        Likes.objects.create(user=self.user, album=self.album)
        # Trying to like the same album again should fail
        with self.assertRaises(Exception):
            Likes.objects.create(user=self.user, album=self.album)

class PhotoViewTestCase(TestCase):
    def setUp(self):
        self.test_image = make_test_image();
        self.user = User.objects.create(email="user@example.com", display_name="coolerputt003")
        self.album = Album.objects.create(user=self.user, album_name="Album 1")
        self.photo = Photo.objects.create(album=self.album, photo_name="Photo 1", photo_img=self.test_image)

    def test_photo_view_count(self):
        view = PhotoView.objects.create(photo=self.photo, count=5)
        self.assertEqual(view.count, 5)
        self.assertEqual(view.photo, self.photo)