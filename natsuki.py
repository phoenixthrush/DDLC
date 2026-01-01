from PIL import Image


def load_natsuki_image(image_path):
    try:
        return Image.open(image_path)
    except IOError:
        print("Error: Unable to load image at", image_path)
        return None


def negate_image(image):
    return Image.eval(image, lambda x: 255 - x)


def flip_and_negate_image(image_path, output_path):
    try:
        with Image.open(image_path) as img:
            negated_img = negate_image(img)
            flipped_img = negated_img.transpose(Image.FLIP_TOP_BOTTOM)

            flipped_img.save(output_path)
            print(f"Processed image saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


def convert_to_polar(image):
    # TODO
    return image


if __name__ == "__main__":
    image_path = "staged/natsuki/0_natsuki.jpg"

    natsuki_image = load_natsuki_image(image_path)
    negated_image = negate_image(natsuki_image).save("staged/natsuki/1_negated.jpg")
    print("Negated image saved to: staged/natsuki/1_negated.jpg")

    flipped_image = (
        Image.open("staged/natsuki/1_negated.jpg")
        .transpose(Image.FLIP_TOP_BOTTOM)
        .save("staged/natsuki/2_flipped.jpg")
    )
    print("Flipped image saved to: staged/natsuki/2_flipped.jpg")

    polar_image = convert_to_polar(Image.open("staged/natsuki/2_flipped.jpg"))
    polar_image.save("staged/natsuki/3_polar.jpg")
    print("Polar converted image saved to: staged/natsuki/3_polar.jpg")
