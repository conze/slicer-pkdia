import slicer
from slicer.i18n import tr as _  # noqa
from slicer.i18n import translate  # noqa
from slicer.ScriptedLoadableModule import (
    ScriptedLoadableModule,
    ScriptedLoadableModuleTest,
    ScriptedLoadableModuleWidget,
)
from SlicerPKDIALib import InstallLogic, SegmentationLogic, Widget


class SlicerPKDIA(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("SlicerPKDIA")
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Segmentation")]
        self.parent.dependencies = []
        self.parent.contributors = ["Pierre-Henri Conze (IMT Atlantique)", "Jonathan Bouyer (Kitware SAS)"]

        self.parent.helpText = _(
            """
            This extension allows the use of the PKDIA neural network in 3DSlicer.<br><br>
            This neural network allows for segmentation of polycystic kidneys in T2 MRI and CT modalities.<br>
            The segmentation is performed on a volume loaded into 3DSlicer, and provides the results as a 3DSlicer segmentation.
            """
        )
        self.parent.acknowledgementText = _(
            "This module is based on the "
            '<a href="https://github.com/conze/pkdia">pkdia repository</a> '
            "developed at "
            '<a href="https://www.imt-atlantique.fr/fr">IMT Atlantique</a>'
        )


class SlicerPKDIAWidget(ScriptedLoadableModuleWidget):
    def __init__(self, parent=None) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.__init__(self, parent)

        self.widget = None

    def setup(self) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.setup(self)

        self.widget = Widget(SegmentationLogic(), InstallLogic())
        self.layout.addWidget(self.widget)


class SlicerPKDIATest(ScriptedLoadableModuleTest):
    def runTest(self):
        from pathlib import Path

        try:
            from SlicerPythonTestRunnerLib import (
                RunnerLogic,
                RunSettings,
                isRunningInTestMode,
            )
        except ImportError:
            slicer.util.warningDisplay("Please install SlicerPythonTestRunner extension to run the self tests.")
            return
        InstallLogic().setupPythonRequirements()

        currentDirTest = Path(__file__).parent.joinpath("Testing")
        results = RunnerLogic().runAndWaitFinished(
            currentDirTest,
            RunSettings(extraPytestArgs=RunSettings.pytestFileFilterArgs("*TestCase.py") + ["-m not slow"]),
            doRunInSubProcess=not isRunningInTestMode(),
        )

        if results.failuresNumber:
            raise AssertionError(f"Test failed: \n{results.getFailingCasesString()}")

        slicer.util.delayDisplay(f"Tests OK. {results.getSummaryString()}")
