import pyrosetta
from pyrosetta.rosetta.protocols.carbohydrates import SimpleGlycosylateMover
from pyrosetta.rosetta.core.pose.carbohydrates import glycosylate_pose
from pyrosetta.rosetta.core.pack.task.operation import (
    InitializeFromCommandline,
    RestrictToRepacking,
)
from pyrosetta.rosetta.core.select.residue_selector import (
    ResidueIndexSelector,
    NeighborhoodResidueSelector,
)
from pyrosetta.rosetta.core.simple_metrics.metrics import RMSDMetric
from pyrosetta.rosetta.core.pack.task.operation import (
    OperateOnResidueSubset,
    PreventRepackingRLT,
)
from pyrosetta.rosetta.protocols.rigid import (
    RigidBodyPerturbNoCenterMover as RBPNCMover,
)
from pyrosetta.rosetta.protocols.relax import FastRelax
from pyrosetta.rosetta.core.select.movemap import MoveMapFactory

## Full imports of libraries 
from pyrosetta.rosetta.core.scoring.constraints import *
from pyrosetta.rosetta.protocols.carbohydrates import *
from pyrosetta.rosetta.core.scoring import *

## ***************************************************************
from pyrosetta.rosetta.core.select.residue_selector import (
    AndResidueSelector, 
    NeighborhoodResidueSelector, 
    NotResidueSelector,
    ChainSelector
)

from pyrosetta.rosetta.core.pack.task import TaskFactory

from pyrosetta.rosetta.protocols.denovo_design.movers import FastDesign

from pyrosetta.rosetta.core.pack.task.operation import (
    PreventRepackingRLT, 
    OperateOnResidueSubset, 
    RestrictToRepackingRLT,
    IncludeCurrent
)

pyrosetta.init("-include_sugars -lock_rings -maintain_links -auto_detect_glycan_connections -alternate_3_letter_codes pdb_sugar -auto_setup_metals -constraints:cst_fa_file ../starting_structure/6N1B_catalytic_and_specific.cst")

pose = pyrosetta.pose_from_pdb("../starting_structure/6N1B-A_antigen.pdb")

sfxn = pyrosetta.create_score_function("ref2015_cart.wts")
inital_energy = sfxn(pose)

sfxn.set_weight(atom_pair_constraint, 1.0)
add_fa_constraints_from_cmdline(pose, sfxn)

sfxn.show(pose)

aa_res = ChainSelector("A")
sugar_res = NotResidueSelector(ChainSelector("A"))

nbr_selector = NeighborhoodResidueSelector(sugar_res, 8, True)
not_to_design = AndResidueSelector(sugar_res, nbr_selector)
only_to_design = NotResidueSelector(not_to_design)
disable_packing = PreventRepackingRLT()
repack_only = RestrictToRepackingRLT()


repack_nbr = OperateOnResidueSubset(
    repack_only, nbr_selector, flip_subset=False
)
nopack_sugar = OperateOnResidueSubset(
    disable_packing, sugar_res, flip_subset=False
)

tf = TaskFactory()
tf.push_back(InitializeFromCommandline())
tf.push_back(IncludeCurrent())
tf.push_back(repack_nbr)
tf.push_back(nopack_sugar)

packer_task = tf.create_task_and_apply_taskoperations(pose)
# View the PackerTask
print(packer_task)

mmf = MoveMapFactory()
mmf.all_bb(True)
mmf.all_chi(True)
mmf.add_bb_action(
    pyrosetta.rosetta.core.select.movemap.move_map_action.mm_disable,
    only_to_design
)
mm = mmf.create_movemap_from_pose(pose)

print(mm)

fd = FastDesign()
fd.set_scorefxn(sfxn)
fd.cartesian(True)
fd.set_task_factory(tf)
fd.set_movemap_factory(mmf)
fd.minimize_bond_angles(True)
fd.minimize_bond_lengths(True)
fd.min_type("lbfgs_armijo_nonmonotone")
fd.max_iter(1)

fd.apply(pose)

