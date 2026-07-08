from pathlib import Path

project_root = (Path(__file__) / ".." / "..").resolve()
src_dir = project_root / "pddlgym"
pddl_dir = src_dir / "pddl"
prompts_dir = src_dir / "prompts"
pddlgym_domain_prompts_dir = prompts_dir / "domains"
pddlgym_problem_prompts_dir = prompts_dir / "problems"
pddlgym_action_prompts_dir = prompts_dir / "actions"
pddlgym_object_names_prompts_dir = prompts_dir / "objects"
