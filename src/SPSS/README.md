# SPSS Files

Unfortunately, there is no good way to automate SPSS runs. In particular, you will
always need to use the mouse to say which data set the various pieces of code should
run on.

For SPSS, please export the syntax file of your analysis and add it to this folder with
a name that follows the format: `###_Description_Of_File.sps` where `###` is a unique
id indicating the order the files should be run in and `Description_Of_File` is a
very brief description.

If you have multiple analyses, feel free to create a folder of syntax files named in
the format: `###_Description_Of_Files` where `###` indicates the order the files should
be run in and `Description_Of_Files` is a very brief description.

Note that in both cases, we recommend the first digit represent a "section" of the
overall analysis. the second digit represent a single analysis, and the third digit is
used sparingly to add additional analyses.

As you add files to this folder, please fill out the following template for
that file in this README.

## Template

### Name of File

A brief description of the file's purpose, e.g., "This file runs our main regression:
Are people who live in the ZIP codes of interest more or less likely to get a COVID
test. It also runs the following robustness checks..."

#### Running this code

A description of how to run this code. For example:

* Place the files called `Survey_Round1.sav` and `Survey_Round2.sav` from our private
  data repository into the `data` folder.
* Click `File > Open > ....`
* Then click `File > Open > ...`
* Then click `Run...`

