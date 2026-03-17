from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):

    bio = models.TextField(blank=True)

    profile_picture = models.ImageField(
        upload_to='profile_picture/',
        blank=True
    )
    dob = models.DateField(null=True,blank=True)

    is_private = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username
    # str is used for readability


    def followers_count(self):
        return self.followers.count()
    def following_count(self):
        return self.following.count()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes =[
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
        ]




class follow(models.Model):

    follower = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="following"
    )

    following = models.ForeignKey(
        CustomUser,
            on_delete=models.CASCADE,
        related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints =[
            models.UniqueConstraint(
                fields=["follower","following"],
                name="Unique_follow_relationship"
            )
        ]
        indexes =[
            models.Index(fields=["follower"]),
            models.Index(fields=["following"]),
        ]



    def clean(self):
        if self.follower == self.following:
            raise ValidationError("User cannot follow themselves.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"
    
    