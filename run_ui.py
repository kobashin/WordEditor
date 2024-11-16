import sys
import os
import pandas as pd
import PyQt5
from PyQt5 import QtWidgets
from WordEditor import Ui_Form

# This is required to run the PyQt5 application in the virtual environment.
# get the parent directory of the PyQt5 package
# reference : https://zenn.dev/eqs/scraps/714b7889323109
# Set the QT_QPA_PLATFORM_PLUGIN_PATH environment variable
dirname = os.path.dirname(PyQt5.__path__[0])
plugin_path = os.path.join(dirname, 'PyQt5', 'Qt5', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class Test(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Test, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        """
            This class has df corresponding to the word_database.csv
            read word_database.csv by pandas
                use first row as header
                encoding is utf-8
                read each column as a string
        """
        # get the list of word_database.csv files in the current directory
        files = os.listdir('.')
        files = [file for file in files if file.startswith('word_database') and file.endswith('.csv')]
        files.sort(reverse=True)
        # get the latest file

        # read the latest file
        self.df = pd.read_csv(files[0],
                              header=0,
                              encoding='utf-8',
                              dtype=str)

        # index to specify the current word
        self.index = 0

    def slot1(self):
        # get the 'definition' column
        definitions = self.df['Definition']

        # search from definitions[0] to definitions[end]
        # and find the first low which doesn't have a value
        for i in range(len(definitions)):
            if pd.isna(definitions[i]):
                self.index = i
                break

        # show the contents of the line at the index
        self.showLineContents(self.index)

    def slot2(self):
        """
        Replace df values with the data on the UI
        """
        self.df.at[self.index, 'Word'] = self.ui.lineEdit.text()
        self.df.at[self.index, 'Date'] = self.ui.lineEdit_2.text()
        self.df.at[self.index, 'Page'] = self.ui.lineEdit_3.text()
        self.df.at[self.index, 'Count'] = self.ui.lineEdit_4.text()
        self.df.at[self.index, 'Definition'] = self.ui.textEdit.toPlainText()
        self.df.at[self.index, 'Example'] = self.ui.textEdit_2.toPlainText()
        self.df.at[self.index, 'Text'] = self.ui.textEdit_3.toPlainText()
        self.df.at[self.index, 'Synonym'] = self.ui.textEdit_4.toPlainText()
        self.df.at[self.index, 'WordFinder'] = self.ui.textEdit_5.toPlainText()
        self.df.at[self.index, 'Memo'] = self.ui.textEdit_6.toPlainText()

    def slot3(self):
        """
        Read the next word from the word_database.csv
        """
        for i in range(self.index + 1, len(self.df['Definition'])):
            if pd.isna(self.df['Definition'][i]):
                self.index = i
                break

        # show the contents of the line at the index
        self.showLineContents(self.index)

    def slot4(self):
        """
        Save the df and lose the application
        """
        # set the file of the output
        fileName = 'word_database_{}.csv'.format(pd.Timestamp.now().strftime('%Y%m%d%H%M%S'))
        
        # save the df to the word_database.csv
        self.df.to_csv(fileName, index=False)
        self.close()

    def showLineContents(self, index):
        """
        Show the contents of the line at the index on the UI

        Args:
            index (int): The index of the line to be shown
        """

        # get the word from the columns
        word = self.df['Word'][index] if not pd.isna(self.df['Word'][index]) else ''
        date = self.df['Date'][index] if not pd.isna(self.df['Date'][index]) else ''
        page = self.df['Page'][index] if not pd.isna(self.df['Page'][index]) else ''
        count = self.df['Count'][index] if not pd.isna(self.df['Count'][index]) else ''
        definition = self.df['Definition'][index] if not pd.isna(self.df['Definition'][index]) else ''
        example = self.df['Example'][index] if not pd.isna(self.df['Example'][index]) else ''
        text = self.df['Text'][index] if not pd.isna(self.df['Text'][index]) else ''
        synonym = self.df['Synonym'][index] if not pd.isna(self.df['Synonym'][index]) else ''
        wordFinder = self.df['WordFinder'][index] if not pd.isna(self.df['WordFinder'][index]) else ''
        memo = self.df['Memo'][index] if not pd.isna(self.df['Memo'][index]) else ''

        # set the word to the lineEdit
        self.ui.lineEdit.setText(word)
        self.ui.lineEdit_2.setText(date)
        self.ui.lineEdit_3.setText(page)
        self.ui.lineEdit_4.setText(count)
        self.ui.textEdit.setText(definition)
        self.ui.textEdit_2.setText(example)
        self.ui.textEdit_3.setText(text)
        self.ui.textEdit_4.setText(synonym)
        self.ui.textEdit_5.setText(wordFinder)
        self.ui.textEdit_6.setText(memo)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec_())
