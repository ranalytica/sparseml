import pytest

from abc import ABC
import time
import numpy
import torch

from neuralmagicML.pytorch.recal import PythonLogger, TensorboardLogger


@pytest.mark.parametrize("logger", [PythonLogger(), TensorboardLogger()])
class TestModifierLogger(ABC):
    def test_name(self, logger):
        assert logger.name is not None

    def test_log_hyperparams(self, logger):
        logger.log_hyperparams({"param1": 0.0, "param2": 1.0})

    def test_log_scalar(self, logger):
        logger.log_scalar("test-scalar-tag", 0.1)
        logger.log_scalar("test-scalar-tag", 0.1, 1)
        logger.log_scalar("test-scalar-tag", 0.1, 2, time.time() - 1)

    def test_log_scalars(self, logger):
        logger.log_scalars("test-scalars-tag", {"scalar1": 0.0, "scalar2": 1.0})
        logger.log_scalars("test-scalars-tag", {"scalar1": 0.0, "scalar2": 1.0}, 1)
        logger.log_scalars(
            "test-scalars-tag", {"scalar1": 0.0, "scalar2": 1.0}, 2, time.time() - 1
        )

    def test_log_histogram(self, logger):
        logger.log_histogram("test-histogram-tag", torch.randn(1000))
        logger.log_histogram("test-histogram-tag", torch.randn(1000), 1)
        logger.log_histogram(
            "test-histogram-tag", torch.randn(1000), 2, time.time() - 1
        )

    def test_log_histogram_raw(self, logger):
        vals = torch.randn(1000).tolist()
        squared_vals = [val * val for val in vals]
        counts, limits = numpy.histogram(vals)
        logger.log_histogram_raw(
            "test-histogram-tag",
            min(vals),
            max(vals),
            len(vals),
            sum(vals),
            sum(squared_vals),
            limits[1:].tolist(),
            counts.tolist(),
        )
        logger.log_histogram_raw(
            "test-histogram-tag",
            min(vals),
            max(vals),
            len(vals),
            sum(vals),
            sum(squared_vals),
            limits[1:].tolist(),
            counts.tolist(),
            1,
        )
        logger.log_histogram_raw(
            "test-histogram-tag",
            min(vals),
            max(vals),
            len(vals),
            sum(vals),
            sum(squared_vals),
            limits[1:].tolist(),
            counts.tolist(),
            2,
            time.time() - 1,
        )