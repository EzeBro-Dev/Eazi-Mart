from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "reviews"
        ordering = ["-created_at"]


    def __str__(self):
        return f"{self.user.username}'s Review on {self.product.name}"


class SellerReview(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_reviews")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_reviews")
    rating = models.IntegerField(default=0)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "seller_reviews"
        ordering = ["-created_at"]


    def __str__(self):
        return f"{self.reviewer.username}'s review of seller {self.seller.username}"



class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="review_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "review_images"
        ordering = ["-uploaded_at"]


    def __str__(self):
        return f"Image for Review #{self.review.id}"

    


class HelpfulReview(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="helpful_reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_helpful = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "helpful_reviews"
        ordering = ["-created_at"]


    def __str__(self):
        return f"{self.user.username} marked review {self.review.id} as helpful"