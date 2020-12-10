# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TODO: Add a description here."""

from __future__ import absolute_import, division, print_function

import glob
import os

import pandas as pd

import datasets


_CITATION = """\
@misc{friedrich2020sofcexp,
      title={The SOFC-Exp Corpus and Neural Approaches to Information Extraction in the Materials Science Domain},
      author={Annemarie Friedrich and Heike Adel and Federico Tomazic and Johannes Hingerl and Renou Benteau and Anika Maruscyk and Lukas Lange},
      year={2020},
      eprint={2006.03039},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
The SOFC-Exp corpus consists of 45 open-access scholarly articles annotated by domain experts.
A corpus and an inter-annotator agreement study demonstrate the complexity of the suggested
named entity recognition and slot filling tasks as well as high annotation quality is presented
in the accompanying paper.
"""

_HOMEPAGE = "https://arxiv.org/abs/2006.03039"

_LICENSE = ""

_URL = "https://github.com/boschresearch/sofc-exp_textmining_resources/archive/master.zip"


class SOFCMaterialsArticles(datasets.GeneratorBasedBuilder):
    """"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "text": datasets.Value("string"),
                "sentence_offsets": datasets.features.Sequence(
                    {"begin_char_offset": datasets.Value("int64"), "end_char_offset": datasets.Value("int64")}
                ),
                "sentences": datasets.features.Sequence(datasets.Value("string")),
                "sentence_labels": datasets.features.Sequence(datasets.Value("int64")),
                "token_offsets": datasets.features.Sequence(
                    {
                        "offsets": datasets.features.Sequence(
                            {"begin_char_offset": datasets.Value("int64"), "end_char_offset": datasets.Value("int64")}
                        )
                    }
                ),
                "tokens": datasets.features.Sequence(datasets.features.Sequence(datasets.Value("string"))),
                "entity_labels": datasets.features.Sequence(
                    datasets.features.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "B-DEVICE",
                                "B-EXPERIMENT",
                                "B-MATERIAL",
                                "B-VALUE",
                                "I-DEVICE",
                                "I-EXPERIMENT",
                                "I-MATERIAL",
                                "I-VALUE",
                                "O",
                            ]
                        )
                    )
                ),
                "slot_labels": datasets.features.Sequence(
                    datasets.features.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "B-anode_material",
                                "B-cathode_material",
                                "B-conductivity",
                                "B-current_density",
                                "B-degradation_rate",
                                "B-device",
                                "B-electrolyte_material",
                                "B-experiment_evoking_word",
                                "B-fuel_used",
                                "B-interlayer_material",
                                "B-interconnect_material",
                                "B-open_circuit_voltage",
                                "B-power_density",
                                "B-resistance",
                                "B-support_material",
                                "B-thickness",
                                "B-time_of_operation",
                                "B-voltage",
                                "B-working_temperature",
                                "I-anode_material",
                                "I-cathode_material",
                                "I-conductivity",
                                "I-current_density",
                                "I-degradation_rate",
                                "I-device",
                                "I-electrolyte_material",
                                "I-experiment_evoking_word",
                                "I-fuel_used",
                                "I-interlayer_material",
                                "I-interconnect_material",
                                "I-open_circuit_voltage",
                                "I-power_density",
                                "I-resistance",
                                "I-support_material",
                                "I-thickness",
                                "I-time_of_operation",
                                "I-voltage",
                                "I-working_temperature",
                                "O",
                            ]
                        )
                    )
                ),
                "links": datasets.Sequence(
                    {
                        "relation_label": datasets.features.ClassLabel(
                            names=["coreference", "experiment_variation", "same_experiment", "thickness"]
                        ),
                        "start_span_id": datasets.Value("int64"),
                        "end_span_id": datasets.Value("int64"),
                    }
                ),
                "slots": datasets.features.Sequence(
                    {
                        "frame_participant_label": datasets.features.ClassLabel(
                            names=[
                                "anode_material",
                                "cathode_material",
                                "current_density",
                                "degradation_rate",
                                "device",
                                "electrolyte_material",
                                "fuel_used",
                                "interlayer_material",
                                "open_circuit_voltage",
                                "power_density",
                                "resistance",
                                "support_material",
                                "time_of_operation",
                                "voltage",
                                "working_temperature",
                            ]
                        ),
                        "slot_id": datasets.Value("int64"),
                    }
                ),
                "spans": datasets.features.Sequence(
                    {
                        "span_id": datasets.Value("int64"),
                        "entity_label": datasets.features.ClassLabel(names=["", "DEVICE", "MATERIAL", "VALUE"]),
                        "sentence_id": datasets.Value("int64"),
                        "experiment_mention_type": datasets.features.ClassLabel(
                            names=["", "current_exp", "future_work", "general_info", "previous_work"]
                        ),
                        "begin_char_offset": datasets.Value("int64"),
                        "end_char_offset": datasets.Value("int64"),
                    }
                ),
                "experiments": datasets.features.Sequence(
                    {
                        "experiment_id": datasets.Value("int64"),
                        "span_id": datasets.Value("int64"),
                        "slots": datasets.features.Sequence(
                            {
                                "frame_participant_label": datasets.features.ClassLabel(
                                    names=[
                                        "anode_material",
                                        "cathode_material",
                                        "current_density",
                                        "degradation_rate",
                                        "conductivity",
                                        "device",
                                        "electrolyte_material",
                                        "fuel_used",
                                        "interlayer_material",
                                        "open_circuit_voltage",
                                        "power_density",
                                        "resistance",
                                        "support_material",
                                        "time_of_operation",
                                        "voltage",
                                        "working_temperature",
                                    ]
                                ),
                                "slot_id": datasets.Value("int64"),
                            }
                        ),
                    }
                ),
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        my_urls = _URL
        data_dir = dl_manager.download_and_extract(my_urls)

        data_dir = os.path.join(data_dir, "sofc-exp_textmining_resources-master/sofc-exp-corpus")

        metadata = pd.read_csv(os.path.join(data_dir, "SOFC-Exp-Metadata.csv"), sep="\t")

        text_base_path = os.path.join(data_dir, "texts")

        text_files_available = [
            os.path.split(i.rstrip(".txt"))[-1] for i in glob.glob(os.path.join(text_base_path, "*.txt"))
        ]

        metadata = metadata[metadata["name"].map(lambda x: x in text_files_available)]

        names = {}
        splits = ["train", "test", "dev"]
        for split in splits:
            names[split] = metadata[metadata["set"] == split]["name"].tolist()

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "names": names["train"],
                    "data_dir": data_dir,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"names": names["test"], "data_dir": data_dir, "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "names": names["dev"],
                    "data_dir": data_dir,
                    "split": "validation",
                },
            ),
        ]

    def _generate_examples(self, names, data_dir, split):
        """ Yields examples. """

        textfile_base_path = os.path.join(data_dir, "texts")
        annotations_base_path = os.path.join(data_dir, "annotations")
        sentence_meta_base_path = os.path.join(annotations_base_path, "sentences")
        tokens_meta_base_path = os.path.join(annotations_base_path, "tokens")
        ets_meta_base_path = os.path.join(annotations_base_path, "entity_types_and_slots")
        frame_meta_base_path = os.path.join(annotations_base_path, "frames")

        sentence_meta_header = ["sentence_id", "label", "begin_char_offset", "end_char_offset"]

        tokens_meta_header = ["sentence_id", "token_id", "begin_char_offset", "end_char_offset"]

        ets_meta_header = [
            "sentence_id",
            "token_id",
            "begin_char_offset",
            "end_char_offset",
            "entity_label",
            "slot_label",
        ]

        for id_, name in enumerate(names):

            textfile_path = os.path.join(textfile_base_path, name + ".txt")
            text = open(textfile_path, encoding="utf-8").read()

            sentence_meta_path = os.path.join(sentence_meta_base_path, name + ".csv")
            sentence_meta = pd.read_csv(sentence_meta_path, sep="\t", names=sentence_meta_header)

            tokens_meta_path = os.path.join(tokens_meta_base_path, name + ".csv")
            tokens_meta = pd.read_csv(tokens_meta_path, sep="\t", names=tokens_meta_header)

            ets_meta_path = os.path.join(ets_meta_base_path, name + ".csv")
            ets_meta = pd.read_csv(ets_meta_path, sep="\t", names=ets_meta_header)

            entity_labels = ets_meta.groupby("sentence_id").apply(lambda x: x["entity_label"].tolist()).to_list()
            slot_labels = ets_meta.groupby("sentence_id").apply(lambda x: x["slot_label"].tolist()).to_list()

            token_offsets = (
                tokens_meta.groupby("sentence_id")[["begin_char_offset", "end_char_offset"]]
                .apply(lambda x: x.to_dict(orient="records"))
                .tolist()
            )

            frames_meta_path = os.path.join(frame_meta_base_path, name + ".csv")
            frames_meta = open(frames_meta_path, encoding="utf-8").readlines()

            sentence_offsets = (
                sentence_meta[["begin_char_offset", "end_char_offset"]].apply(lambda x: x.to_dict(), axis=1).tolist()
            )

            sentence_labels = sentence_meta["label"].tolist()

            sentences = [text[ost["begin_char_offset"] : ost["end_char_offset"]] for ost in sentence_offsets]

            tokens = [
                [s[tto["begin_char_offset"] : tto["end_char_offset"]] for tto in to]
                for s, to in zip(sentences, token_offsets)
            ]

            experiment_starts = [i for i, line in enumerate(frames_meta) if line.startswith("EXPERIMENT")]
            experiment_start = min(experiment_starts)
            link_start = min([i for i, line in enumerate(frames_meta) if line.startswith("LINK")])

            spans_raw = frames_meta[:experiment_start]

            spans = []
            for span in spans_raw:
                _, span_id, entity_label_or_exp, sentence_id, begin_char_offset, end_char_offset = span.split("\t")

                if entity_label_or_exp.startswith("EXPERIMENT"):
                    exp, experiment_mention_type = entity_label_or_exp.split(":")
                    entity_label = ""
                else:
                    entity_label = entity_label_or_exp
                    exp = ""
                    experiment_mention_type = ""

                s = {
                    "span_id": span_id,
                    "entity_label": entity_label,
                    "sentence_id": sentence_id,
                    "experiment_mention_type": experiment_mention_type,
                    "begin_char_offset": int(begin_char_offset),
                    "end_char_offset": int(end_char_offset),
                }
                spans.append(s)

            links_raw = [f.rstrip("\n") for f in frames_meta[link_start:]]

            links = []
            for l in links_raw:
                _, relation_label, start_span_id, end_span_id = l.split("\t")

                link_out = {
                    "relation_label": relation_label,
                    "start_span_id": int(start_span_id),
                    "end_span_id": int(end_span_id),
                }
                links.append(link_out)

            experiments = []
            for start, end in zip(experiment_starts[:-1], experiment_starts[1:]):
                current_experiment = frames_meta[start:end]
                _, experiment_id, span_id = current_experiment[0].rstrip("\n").split("\t")
                exp = {"experiment_id": int(experiment_id), "span_id": int(span_id)}

                slots = []
                for e in current_experiment[1:]:
                    e = e.rstrip("\n")
                    _, frame_participant_label, slot_id = e.split("\t")
                    to_add = {"frame_participant_label": frame_participant_label, "slot_id": int(slot_id)}
                    slots.append(to_add)
                exp["slots"] = slots

                experiments.append(exp)

            yield id_, {
                "text": text,
                "sentence_offsets": sentence_offsets,
                "sentences": sentences,
                "sentence_labels": sentence_labels,
                "token_offsets": [{"offsets": to} for to in token_offsets],
                "tokens": tokens,
                "entity_labels": entity_labels,
                "slot_labels": slot_labels,
                "links": links,
                "slots": slots,
                "spans": spans,
                "experiments": experiments,
            }
