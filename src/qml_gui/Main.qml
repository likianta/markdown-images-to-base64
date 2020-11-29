import QtQuick 2.15
import LightClean 1.0
import LightClean.LCButtons 1.0

LCWindow {
    width: 500; height: 100
    p_color: '#f2f2f2'

    property alias  p_ifile: _row1.p_path
    property string p_ofile: PyHandler.call('calc_target', p_ifile)

    LCFileBrowse {
        id: _row1
        anchors {
            left: parent.left
            leftMargin: 20
            right: parent.right
            rightMargin: 20
            top: parent.top
            topMargin: 10
        }
        clip: true
        width: 300; height: 30
        p_borderless: false
        p_dialogTitle: 'Select a .md or .html (from Typora exported) file'
        p_filetype: ['Markdown file (*.md)', 'HTML file (*.html)']
        p_hint: 'Put .md or .html file here'
        p_title: 'Input:'
    }

    LCRow {
        id: _row2
        anchors {
            left: parent.left
            leftMargin: 20
            right: parent.right
            rightMargin: 20
            top: _row1.bottom
            topMargin: 10
        }
        height: 30

        LCButton {
            p_borderless: false
            p_text: 'Run'
            onClicked: PyHandler.call('run', p_ifile)
            // onClicked: {  // TEST
            //     _openBtn.enabled = true
            // }
        }

        LCButton {
            id: _openBtn
            enabled: PyHandler.call('target_file_exists', p_ofile)  // bool
            p_borderless: false
            p_text: 'Open'

            onClicked: PyHandler.call('open_target', p_ofile)

            states: [
                State {
                    when: !_openBtn.enabled
                    PropertyChanges {
                        target: _openBtn
                        p_color: '#cccccc'
                    }
                }
            ]
        }
    }
}
