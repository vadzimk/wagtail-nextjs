# https://docs.wagtail.org/en/stable/topics/streamfield.html#streamfield-topic

from wagtail.core.blocks import (BooleanBlock,
                                 CharBlock,
                                 ChoiceBlock,
                                 DateTimeBlock,
                                 FieldBlock,
                                 IntegerBlock,
                                 ListBlock,
                                 PageChooserBlock,
                                 RawHTMLBlock,
                                 RichTextBlock,
                                 StreamBlock,
                                 StructBlock,
                                 StructValue,
                                 TextBlock,
                                 URLBlock
                                 )
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.blocks import ImageChooserBlock


class CustomImageChooserBlock(ImageChooserBlock):
    # chooser block is for object selection
    def __init__(self, *args, **kwargs):
        self.rendition = kwargs.pop('rendition', 'original')
        super(CustomImageChooserBlock, self).__init__(**kwargs)

    def get_api_representation(self, value, context=None):
        return ImageRenditionField(self.rendition).to_representation(value)



class ImageText(StructBlock):
    # StructBlock works like dict
    reverse = BooleanBlock(required=False)
    text = RichTextBlock()
    image = CustomImageChooserBlock(rendition='width-800')


class BodyBlock(StreamBlock):
    # StreamBlock works like array
    h1 = CharBlock()
    h2 = CharBlock()
    paragraph = RichTextBlock()
    image_text = ImageText()
    image_carousel = ListBlock(CustomImageChooserBlock())
    thumbnail_gallery = ListBlock(CustomImageChooserBlock())

