# Short Word-Form Normalization
This project contains scripts to normalize sms text messeges.
All folders contain means to split the data, train and evaluate.

1. The folder *aligned corpus* contains scrips that are applied on aligned data.
   An example for an aligned sentence is:

   **SMS**: ##u^#r#^go#na^##^##c

   **ENG**:  you^are^going^to^see

   in which spaces are marked as '^' and fillers on sms side are '#'
   - To align the data I slightly modified the script found here:

     http://www.giovannicarmantini.com/2016/01/minimum-edit-distance-in-python

     In *align* folder you can align parallel sentences.

2. The folder *non-aligned corpus* contains scripts to non-aligned evaluate data
   (training can be done with the same files as in the *aligned corpus* folder).
   An example for a non-aligned sentence is:

   **SMS**: u^r^gonna^c

   **ENG**: you^are^going^to^see

3. The folder *linear kernel* will be described soon.
