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
from wagtail.images.blocks import ImageChooserBlock


class CustomImageChooserBlock(ImageChooserBlock):
    # chooser block is for object selection
    pass


class ImageText(StructBlock):
    # StructBlock works like dict
    reverse = BooleanBlock(required=False)
    text = RichTextBlock()
    image = CustomImageChooserBlock()


class BodyBlock(StreamBlock):
    # StreamBlock works like array
    h1 = CharBlock()
    h2 = CharBlock()
    paragraph = RichTextBlock()
    image_text = ImageText()
    image_carousel = ListBlock(CustomImageChooserBlock())
    thumbnail_gallery = ListBlock(CustomImageChooserBlock())

