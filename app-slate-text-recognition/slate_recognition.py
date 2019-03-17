import cv2
import math
import pytesseract
import re

from clams.serve import ClamApp
from clams.serialize import *
from clams.vocab import AnnotationTypes
from clams.vocab import MediaTypes
from clams.restify import Restifier

class SlateRecognition(ClamApp):

    def appmetadata(self):
        metadata = {"name": "Slate Text Recognition",
                    "description": "This tool recognizes text in detected slates. ",
                    "vendor": "Team CLAMS",
                    "requires": [MediaTypes.V],
                    "produces": [AnnotationTypes.OCR]}
        return metadata

    def sniff(self, mmif):
        # this mock-up method always returns true
        return True

    def annotate(self, mmif_json):
        mmif = Mmif(mmif_json)
        video_filename = mmif.get_medium_location(MediaTypes.V)
        slate_output = self.run_slaterecognition(video_filename, mmif_json) #slate_output is a list of (target, text)

        new_view = mmif.new_view()
        contain = new_view.new_contain(AnnotationTypes.SD)
        contain.producer = self.__class__

        for int_id, (target, text) in enumerate(slate_output):
            annotation = new_view.new_annotation(int_id)
            annotation.target = str(target)
            annotation.features.characters = str(text)
            #annotation.feature = {'conf':confidence}
            annotation.attype = AnnotationTypes.OCR

        for contain in new_view.contains.keys():
            mmif.contains.update({contain: new_view.id})
        return mmif

    @staticmethod
    def run_slaterecognition(video_filename, mmif, stop_after_one=False):

        def get_slate_frame_range(in_mmif):
            frame_range_list = []
            view = in_mmif.get_view_contains(AnnotationTypes.SD)
            for annotation in view:
                frame_range_list.append((annotation.id, annotation.start, annotation.end))
            return frame_range_list

        def process_image(f):
            proc = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            proc = cv2.bitwise_not(proc)
            proc = cv2.threshold(proc, 0, 255,
                                 cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            return proc

        def read_frame(f):
            proc = process_image(f)
            return pytesseract.image_to_string(proc)

        slate_frames = get_slate_frame_range(mmif)
        slate_range = slate_frames[0]
        target_frame = math.floor((slate_range[2]-slate_range[1])/2)
        cap = cv2.VideoCapture(video_filename)
        cap.set(1, target_frame)
        print (target_frame)
        ret, frame = cap.read()
        res = read_frame(frame)
        return ([slate_range[0],res])



if __name__ == "__main__":
    slate_tool = SlateRecognition()
    slate_service = Restifier(slate_tool)
    slate_service.run()

