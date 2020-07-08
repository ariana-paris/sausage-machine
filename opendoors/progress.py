from configparser import ConfigParser
from logging import Logger

from opendoors import step_01, step_02, step_03

steps = {
    '01': {'next': '02', 'name': 'load', 'class': step_01.Step01},
    '02': {'next': '03', 'name': 'load', 'class': step_02.Step02},
    '03': {'next': '04', 'name': 'load', 'class': step_03.Step03}
}


def continue_from_last(config: ConfigParser, logger: Logger):
    step_to_run = get_next_step(config)
    step_config = steps[step_to_run]
    step = step_config['class'](config, logger)
    success = step.run()
    if success:
        config['Processing']['next_step'] = step_config['next']
        done_steps = set(config['Processing']['done_steps'].split(', '))
        if len(done_steps) == 0:
            done_steps = {step_to_run}
        else:
            done_steps.add(step_to_run)
        config['Processing']['done_steps'] = ', '.join(done_steps)
    return success


def get_next_step(config):
    step_to_run = config['Processing']['next_step']
    if step_to_run != "01":
        resume_yn = \
            input(f"Steps {config['Processing']['done_steps']} have already been completed. Please choose one "
                  f"of the following options:\n"
                  f"1. Continue processing from step {config['Processing']['next_step']} (default)\n"
                  f"2. Restart entire process from step 01 "
                  f"(this will remove any working files and databases already created)\n")
        resume = resume_yn.lower() != '2'
    else:
        resume = True
    if not resume:
        step_to_run = "01"
    return step_to_run
