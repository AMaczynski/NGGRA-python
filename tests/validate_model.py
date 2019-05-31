from img_utils.classifier import Classifier
import os

if __name__ == '__main__':
    classifier = Classifier()
    f = open("../validation.txt", "w")
    path = "../test_data"
    images = os.listdir(path)

    for image in images:
        image_path = "%s/%s" % (path, image)
        result = classifier.label_image_from_file(image_path)
        print(image)
        print(result)
        f.write("%s: got %s, %f\n" % (image, result[0][0], result[0][1]))
    f.close()


