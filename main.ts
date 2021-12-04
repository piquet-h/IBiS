let range = 30

bluetooth.onBluetoothConnected(function () {
    basic.showIcon(IconNames.Yes)
})
bluetooth.onBluetoothDisconnected(function () {
    basic.showIcon(IconNames.No)
})
// Initial head direction
function resetHeading () {
    neutralBearing = input.compassHeading()
}
// Calculate delta
function calculateDelta (neutralBearing: number, currentHeading: number) {
    let delta = neutralBearing - currentHeading

    return delta
}
input.onLogoEvent(TouchButtonEvent.Pressed, function () {
    resetHeading()
})

let leftLimitBearing = 0
let rightLimitBearing = 0
let neutralBearing = 0
bluetooth.startUartService()
neutralBearing = input.compassHeading()
basic.forever(function () {
    let delta = calculateDelta(neutralBearing, input.compassHeading())
    bluetooth.uartWriteNumber(delta)
})
