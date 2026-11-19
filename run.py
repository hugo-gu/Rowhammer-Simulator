from pathlib import Path
from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent

runner = get_runner("icarus")
runner.build(
    sources=[HERE / "verilog.v"],
    hdl_toplevel="attacker",
    build_dir=HERE / "sim_build",
)
runner.test(
    hdl_toplevel="attacker",
    test_module="bridge",
    test_dir=HERE,
    build_dir=HERE / "sim_build",
)
