import time

class ChessTimer(object):
  """
  The ChessTimer class provides a timer which measures elapsed time on a
  given task.  There is no limit to the number of tasks, but only one task
  accumulates time at any given moment.

  All times are in floating-point seconds.

  Requires Python ≥ 3.3 because it uses time.monotonic().
  """

  def __init__(self):

    # If the current task is anything other than none, then
    # self._timers[self._current_task] must be defined.
    self._current_task = None
    self._timers = {}

    # This is only updated when there is a change in state, and only method
    # _elapsed is allowed to update it.
    # To get the elapsed time of the current task, use elapsed_time() below.
    self._reftime = time.monotonic()


  # Elapsed time since the last reset.
  # Pass reset=True to reset elapsed time counter.
  # This is the only method that's allowed to touch self._reftime.
  def _elapsed(self, reset=False):
    oldreftime = self._reftime
    newreftime = time.monotonic()
    if reset:
      self._reftime = newreftime

    return newreftime - oldreftime


  # Get current task
  def current_task(self):
    return self._current_task


  # Switch tasks
  # returns the elapsed time from the current task (before the switch)
  def switch_to(self, newtask):
    task = self._current_task
    elapsed = self._elapsed(True)
    if task is not None:
      self._timers[task] += elapsed

    self._current_task = newtask
    if newtask is not None and newtask not in self._timers:
      self._timers[newtask] = 0.0

    if task is not None:
      return self._timers[task]


  # Return the elapsed time for the specified task.
  # task=None to get the elapsed time for the current task.
  # reset=True to simultaneously reset the timer for this task.
  def elapsed_time(self, task=None, reset=False):
    if task is None:
      task = self._current_task
    if task not in self._timers:
      return None

    value = self._timers[task]
    if task == self._current_task:
      value += self._elapsed(reset)

    if reset:
      self._timers[task] = 0.0

    return value


  # Fetch all data points.
  # reset=True to simultaneously reset all timers.
  def all_elapsed_time(self, reset=False):
    values = self._timers.copy()
    elapsed = self._elapsed(reset)
    task = self._current_task
    if task is not None:
        values[task] += elapsed

    if reset:
      self._timers = {}
      if task is not None:
        self._timers[task] = 0.0

    return values
