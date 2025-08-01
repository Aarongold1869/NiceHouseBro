from django.db import models
from profiles.models import Profile

# Create your models here.
class SavedProperty(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    property_id = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.IntegerField()
    image = models.ImageField(upload_to='property_images/', default='property_images/default/shrek.webp')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cap_rate = models.DecimalField(max_digits=7, decimal_places=4)
    beds = models.IntegerField()
    baths = models.DecimalField(max_digits=2, decimal_places=1)
    sq_ft = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint('profile', 'property_id', name='profile-property_id'),
        ]
    
    def __str__(self):
        return f'{self.profile.user.username} - {str(self.property_id)} - {self.timestamp}'
    
    @property
    def endpoint(self):
        return f'/property/detail/state={self.state}&city={self.city}&address={self.address}&zip={self.zip}&id={self.property_id}/'
    
    @property
    def address_full(self):
        return f'{self.address}, {self.city}, {self.state} {self.zip}'