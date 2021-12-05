bluetooth.onBluetoothConnected(function () {
    basic.showIcon(IconNames.Yes)
})
bluetooth.onBluetoothDisconnected(function () {
    basic.showIcon(IconNames.No)
})
input.onButtonPressed(Button.A, function () {
    bluetooth.uartWriteLine("A")
})
input.onButtonPressed(Button.B, function () {
    bluetooth.uartWriteLine("B")
})
bluetooth.startUartService()
