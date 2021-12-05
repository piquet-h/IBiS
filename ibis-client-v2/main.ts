bluetooth.onBluetoothConnected(function () {
    basic.showIcon(IconNames.Yes)
})
bluetooth.onBluetoothDisconnected(function () {
    basic.showIcon(IconNames.No)
})
input.onGesture(Gesture.TiltLeft, function () {
    bluetooth.uartWriteLine("LEFT:")
})
input.onGesture(Gesture.Shake, function () {
    bluetooth.uartWriteLine("SHAKE:")
})
input.onGesture(Gesture.TiltRight, function () {
    bluetooth.uartWriteLine("RIGHT:")
})
let roll = 0
let pitch = 0
bluetooth.startButtonService()
bluetooth.startUartService()
loops.everyInterval(500, function () {
    bluetooth.uartWriteLine(`R:${pitch}:${roll}`)
})
basic.forever(function () {
    pitch = input.rotation(Rotation.Pitch)
    roll = input.rotation(Rotation.Roll)
})
