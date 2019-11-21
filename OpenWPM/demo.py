from __future__ import absolute_import

import logging
import os

from numpy import random
from six.moves import range
from automation import CommandSequence, TaskManager
from sites_by_category_clean import books, pets, antiques

logger = logging.getLogger('openwpm')

# The list of sites that we wish to crawl

NUM_BROWSERS = 3
sites = random.choice(books, 3)

# Loads the default manager params
# and NUM_BROWSERS copies of the default browser params
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):

    #try:
    #    tarpath = os.path.join(manager_params['data_directory'], 'browser_profile')
    #    browser_params[i]['profile_tar'] = tarpath
    #except:
    #    pass

    # Record HTTP Requests and Responses
    browser_params[i]['http_instrument'] = True
    # Record cookie changes
    browser_params[i]['cookie_instrument'] = True
    # Record Navigations
    browser_params[i]['navigation_instrument'] = True
    # Record JS Web API calls
    browser_params[i]['js_instrument'] = True
    # Enable flash for all three browsers
    browser_params[i]['disable_flash'] = True

    browser_params[i]['profile_archive_dir'] = \
        os.path.join(manager_params['data_directory'], 'browser_profile')

#browser_params[0]['headless'] = False  # Launch only browser 0 headless

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/'
manager_params['log_directory'] = '~/Desktop/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites
for site in sites:

    # Parallelize sites over all number of browsers set above.
    # (To have all browsers go to the same sites, add `index='**'`)
    command_sequence = CommandSequence.CommandSequence(site, reset=True)

    # Start by visiting the page
    command_sequence.get(sleep=3, timeout=60)

    # Run commands across the three browsers (simple parallelization)
    manager.execute_command_sequence(command_sequence)

# Shuts down the browsers and waits for the data to finish logging
manager.close()
