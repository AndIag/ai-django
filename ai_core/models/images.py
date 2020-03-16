from django.db import models


class ImageContainerModel(models.Model):
    """Delays image upload until the model is created and has a generated PK."""

    _image_fields = []

    def _delay_image_upload(self):
        """Set all '_image_fields' to None saving the values until the instance is created."""
        delayed = {}
        for field in self._image_fields:
            if getattr(self, field):
                delayed[field] = getattr(self, field)
                setattr(self, field, None)
        return delayed

    def _upload_images(self, images):
        """Upload delayed images"""
        for field in images.keys():
            if images[field]:
                getattr(self, field).save(images[field].name, images[field])

    def save(self, *args, **kwargs):
        if not self.id:
            images = self._delay_image_upload()
            super(ImageContainerModel, self).save(*args, **kwargs)  # Create instance
            self._upload_images(images)
            return
        super(ImageContainerModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
