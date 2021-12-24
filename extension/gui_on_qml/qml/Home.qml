import QtQuick

Window {
    id: root
    color: '#F2F2F2'
    visible: true

    Rectangle {
        id: _rect
        anchors.left: parent.left
        anchors.margins: 24
        anchors.verticalCenter: parent.verticalCenter
        width: 200
        height: 200
        radius: 12
        border.width: 1
        color: '#FFFFFF'
    }

    Rectangle {
        id: _divider
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 24
        width: 1
        color: '#D8D8D8'
    }

    Item {
        id: _output_selector_box
        width: 200 + 40
        height: 200 + 40

        Rectangle {
            id: _main_box
            width: 200
            height: 200
            radius: 12
            border.width: 1
            color: '#FFFFFF'
        }

        Column {
            id: _candidates_box

            anchors.left: _output_selector_box.right
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 24
            spacing: 12

            property real __size: _candidates_box.height / 4
        }
    }
}