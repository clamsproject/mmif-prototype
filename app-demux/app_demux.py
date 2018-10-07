from clams.serve import ClamApp
from clams.serialize import *
from clams.vocab import AnnotationTypes
from clams.vocab import MediaTypes
from clams.restify import Restifier

class Demuxer(ClamApp):

    def appmetadata(self):

        metadata = {"name": "AV de-multiplexer",
                    "description": "This tool extracts audio track from a video file",
                    "vendor": "Team CLAMS",
                    "requires": [MediaTypes.V],
                    "produces": [MediaTypes.A]}
        return metadata

    def sniff(self, mmif):
        return True

    def annotate(self, mmif_json):
        mmif = Mmif(mmif_json)
        video_filename = mmif.get_medium_location(MediaTypes.V)
        audio = Medium(str(len(mmif.media)))
        audio.location = ".".join(video_filename.split(".")[:-1]) + ".wav"
        audio.type = MediaTypes.A
        mmif.add_media(audio)

        return mmif

if __name__ == "__main__":
    demux_tool = Demuxer()
    demux_service = Restifier(demux_tool)
    demux_service.run()
