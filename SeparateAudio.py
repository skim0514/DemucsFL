import torch
from torchaudio.pipelines import HDEMUCS_HIGH_MUSDB_PLUS
from torchaudio.transforms import Fade

from demucs import pretrained
from demucs.apply import apply_model

class SeparateAudio:
    def __init__(self, waveform, sample_rate):
        self.waveform = waveform
        self.sample_rate = sample_rate

        return

    def runSeparation(self):
        # bundle = HDEMUCS_HIGH_MUSDB_PLUS

        model = pretrained.get_model('htdemucs')

        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        #
        # model.to(device)

        self.sample_rate = 44100

        mixture = self.waveform
        mixture = mixture.reshape(1, mixture.shape[0], -1)

        # parameters
        segment: int = 10
        overlap = 0.1

        print("Separating track")

        # sources = self.separate_sources(
        #     model,
        #     waveform[None],
        #     device=device,
        #     segment=segment,
        #     overlap=overlap,
        # )[0]
        # sources = sources * ref.std() + ref.mean()

        sources = apply_model(model, mixture, device=device)[0]

        sources_list = model.sources
        # sources = list(sources)


        audios = dict(zip(sources_list, sources))

        return audios


    # def separate_sources(
    #         self,
    #         model,
    #         mix,
    #         segment=10.,
    #         overlap=0.1,
    #         device=None,
    # ):
    #     """
    #     Apply model to a given mixture. Use fade, and add segments together in order to add model segment by segment.
    #
    #     Args:
    #         segment (int): segment length in seconds
    #         device (torch.device, str, or None): if provided, device on which to
    #             execute the computation, otherwise `mix.device` is assumed.
    #             When `device` is different from `mix.device`, only local computations will
    #             be on `device`, while the entire tracks will be stored on `mix.device`.
    #     """
    #     if device is None:
    #         device = mix.device
    #     else:
    #         device = torch.device(device)
    #
    #     batch, channels, length = mix.shape
    #
    #     chunk_len = int(self.sample_rate * segment * (1 + overlap))
    #     start = 0
    #     end = chunk_len
    #     overlap_frames = overlap * self.sample_rate
    #     fade = Fade(fade_in_len=0, fade_out_len=int(overlap_frames), fade_shape='linear')
    #
    #     final = torch.zeros(batch, len(model.sources), channels, length, device=device)
    #
    #     while start < length - overlap_frames:
    #         chunk = mix[:, :, start:end]
    #         with torch.no_grad():
    #             out = model.forward(chunk)
    #         out = fade(out)
    #         final[:, :, :, start:end] += out
    #         if start == 0:
    #             fade.fade_in_len = int(overlap_frames)
    #             start += int(chunk_len - overlap_frames)
    #         else:
    #             start += chunk_len
    #         end += chunk_len
    #         if end >= length:
    #             fade.fade_out_len = 0
    #     return final


