#!/usr/bin/python
# -*- coding: utf-8 -*-
# font-name-generator.py 
# Copyright (c) 2012, Dave Crossland (dave@understandingfonts.com)
# Copyright (c) 2011, Greg Haskins (contact@greghaskins.com)
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#   The name of the author may not be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
#   WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#   MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
#   EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Based on code from https://github.com/greghaskins/gibberish
"""
A FontForge plug-in to automatically generate font names.

Copy to ~/.FontForge/python/ and then find "Name This Font" in the Tools menu.
"""
import string, itertools, random

vowels = 'aeiou'

initial_consonants = (set(string.ascii_lowercase) - set(vowels)
                      # remove those easily confused with others
                      - set('qxc')
                      # add some crunchy clusters
                      | set(['bl', 'br', 'cl', 'cr', 'dr', 'fl',
                             'fr', 'gl', 'gr', 'pl', 'pr', 'sk',
                             'sl', 'sm', 'sn', 'sp', 'st', 'str',
                             'sw', 'tr', 'oy', 'ji', 'ch', 'fj', 
                             'zh'])
                      )

final_consonants = (set(string.ascii_lowercase) - set(vowels)
                    # confusable
                    - set('qxcj')
                    # crunchy clusters
                    | set(['ct', 'ft', 'mp', 'nd', 'ng', 'nk', 'nt',
                           'pt', 'sk', 'sp', 'ss', 'st', 'oy', 'ji', 
                           'ch', 'ee', 'zz', 'fj', 'tz'])
                    )

# each syllable is consonant-vowel-consonant "pronounceable"
syllables = map(''.join, itertools.product(initial_consonants, 
                                           vowels, 
                                           final_consonants))

def gibberish(wordcount, wordlist=syllables):
    return ''.join(random.sample(wordlist, wordcount))

def nameFont(registerobject, font):
#	We could just set the name with
#	fontName = gibberish(2).title()
#	But we'll ask the user to pick one of 10
	title = 'Name Font'
	question = 'Choose a font name:'
	nameList = []
	for i in range(10):
		nameList.append(gibberish(2).title())
	answers = tuple(nameList)
	choice = fontforge.askChoices(title,question,answers)
	if choice == -1:
		# User pressed cancel
		return
	else:
		fontName = nameList[choice]
		font = fontforge.activeFont()
		# Set PostScript Style Name (FamilyName-Style)
		font.weight = "Regular"
		font.fontname = fontName + '-' + font.weight
		# Set PostScript Family Name (Family Name)
		font.familyname = fontName
		# Set PostScript Full Name (Family Name Style)
		font.fullname = fontName + ' ' + font.weight
		message = "New name:\n" + font.fullname
		fontforge.postNotice("New Name", message)

def shouldWeAppear(registerobject, font):
	if font.fontname[0:8] == "Untitled":
		return True
	else:
		return False

# Hook this into the Tools menu
if fontforge.hasUserInterface():
  #  keyShortcut="Ctl+Shft+n"
  keyShortcut = None
  menuText = "Name This Font"
  fontforge.registerMenuItem(nameFont,shouldWeAppear,None,"Font",keyShortcut,menuText);
