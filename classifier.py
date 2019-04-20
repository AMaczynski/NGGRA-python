from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2

import numpy as np
import tensorflow as tf


class Classifier:
    def __init__(self):
        model_file = "model/output_graph.pb"
        self.graph = self.load_graph(model_file)

        label_file = "model/output_labels.txt"
        self.labels = self.load_labels(label_file)

        input_layer = "Placeholder"
        output_layer = "final_result"
        input_name = "import/" + input_layer
        output_name = "import/" + output_layer
        self.input_operation = self.graph.get_operation_by_name(input_name)
        self.output_operation = self.graph.get_operation_by_name(output_name)

        self.sess = tf.Session(graph=self.graph)

    def load_graph(self, model_file):
        graph = tf.Graph()
        graph_def = tf.GraphDef()

        with open(model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)

        return graph

    def read_tensor_from_image_file(self, file_name,
                                    input_height=299,
                                    input_width=299,
                                    input_mean=0,
                                    input_std=255):
        input_name = "file_reader"
        output_name = "normalized"
        file_reader = tf.read_file(file_name, input_name)
        if file_name.endswith(".png"):
            image_reader = tf.image.decode_png(
                file_reader, channels=3, name="png_reader")
        elif file_name.endswith(".gif"):
            image_reader = tf.squeeze(
                tf.image.decode_gif(file_reader, name="gif_reader"))
        elif file_name.endswith(".bmp"):
            image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
        else:
            image_reader = tf.image.decode_jpeg(
                file_reader, channels=3, name="jpeg_reader")
            float_caster = tf.cast(image_reader, tf.float32)
            dims_expander = tf.expand_dims(float_caster, 0)
            resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
            normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
            sess = tf.Session()
            result = sess.run(normalized)

        return result

    def load_labels(self, label_file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
        return label

    def label_image(self, frame):
        # Format for the Mul:0 Tensor
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        frame = cv2.resize(frame, dsize=(299, 299))
        # Numpy array
        np_image_data = np.asarray(frame)
        np_image_data = cv2.normalize(np_image_data.astype('float'), None, -0.5, .5, cv2.NORM_MINMAX)
        # maybe insert float convertion here - see edit remark!
        np_final = np.expand_dims(np_image_data, axis=0)
        # softmax_tensor = self.sess.graph.get_tensor_by_name('final_result:0')

        # now feeding it into the session:
        # [... initialization of session and loading of graph etc]
        # results = self.sess.run(softmax_tensor,
        #                        {'Mul:0': np_final})
        results = self.sess.run(self.output_operation.outputs[0], {
            self.input_operation.outputs[0]: np_final
        })
        results = np.squeeze(results)
        top_k = results.argsort()[-5:][::-1]

        tops = []
        for i in top_k:
            tops.append((self.labels[i], results[i]))
        return tops

def label_image_from_file(self, file_path):
        input_height = 299
        input_width = 299
        input_mean = 0
        input_std = 255

        t = self.read_tensor_from_image_file(
            file_path,
            input_height=input_height,
            input_width=input_width,
            input_mean=input_mean,
            input_std=input_std)

        results = self.sess.run(self.output_operation.outputs[0], {
            self.input_operation.outputs[0]: t
        })
        results = np.squeeze(results)

        top_k = results.argsort()[-5:][::-1]

        tops = []
        for i in top_k:
            tops.append((self.labels[i], results[i]))
        return tops
