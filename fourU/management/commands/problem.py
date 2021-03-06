# -*- coding: utf-8 -*-

# this file is a modified version of django.core.management.commands.shell,
# and thus licensed under the 3-clause BSD license
# see http://code.djangoproject.com/browser/django/trunk/LICENSE for more details

import os
from django.core.management.base import LabelCommand
from optparse import make_option

class Command(LabelCommand):
	option_list = LabelCommand.option_list
	help = "Runs a Python interactive interpreter. " + \
	       "Doesn't use IPython, since it doesn't like sys.exit(), " + \
	       "and you'll be outputting to a file anyways, or wanting to see straight code."

	requires_model_validation = False

	def handle_label(self, label, **options):
		# XXX: (Temporary) workaround for ticket #1796: force early loading of all
		# models from installed apps.
		from django.db.models.loading import get_models
		loaded_models = get_models()

		use_plain = options.get('plain', False)

		import code
		# Set up a dictionary to serve as the environment for the shell, so
		# that tab completion works on objects that are imported at runtime.
		# See ticket 5082.
		imported_objects = {}
		try: # Try activating rlcompleter, because it's handy.
			import readline
		except ImportError:
			pass
		else:
			# We don't have to wrap the following import in a 'try', because
			# we already know 'readline' was imported successfully.
			import rlcompleter
			readline.set_completer(rlcompleter.Completer(imported_objects).complete)
			readline.parse_and_bind("tab:complete")

		# We want to honor both $PYTHONSTARTUP and .pythonrc.py, so follow system
		# conventions and get $PYTHONSTARTUP first then import user.
		if not use_plain: 
			pythonrc = os.environ.get("PYTHONSTARTUP") 
			if pythonrc and os.path.isfile(pythonrc): 
				try: 
					execfile(pythonrc) 
				except NameError: 
					pass
			# This will import .pythonrc.py as a side-effect
			import user
		#code.interact(local=imported_objects)
		console = code.InteractiveConsole()
		codeObject = compile(file(label).read(), '', 'exec')
		console.runcode(codeObject)
