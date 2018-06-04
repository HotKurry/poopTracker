#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from twython import Twython
import pivot_tools
import random

search = pivot_tools.searchTwitter("Joey doesn't share food", 1)

print pivot_tools.oneGif(search, "joey doesn't share food", "sharefood.gif")

search = pivot_tools.searchTwitter("We were on a break", 1)

print pivot_tools.threeGif(search, "we were on a break", "break_beds.gif", "break_coffees.gif", "break_wife.gif")

search = pivot_tools.searchTwitter("She's your lobster", 1)

print pivot_tools.oneGif(search, "she's your lobster", "shes_lobster.gif")
