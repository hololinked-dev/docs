import 'wot-bundle.min.js';

servient = new Wot.Core.Servient(); 
// Wot.Core is auto-imported by wot-bundle.min.js
servient.addClientFactory(new Wot.Http.HttpsClientFactory({ allowSelfSigned : true }))


servient.start().then(async (WoT) => {
    console.debug("WoT servient started")
    let td = await WoT.requestThingDescription(
                    "https://example.com/spectrometer/resources/wot-td")
    // replace with your own PC hostname
    // /resources/wot-td is a standard endpoint for thing description
    // Thing Descriptions for your devices will be auto-created at this endpoint
    // on each access 

    // ....
    // ....
    spectrometer = await WoT.consume(td);
    console.info("consumed thing description from spectrometer")

    // read and write property
    await spectrometer.writeProperty("serial_number", { "value" : "USB2+H15897"})
    // It is currently a wrong style that one should supply a value to the property
    // using "value" key. This will be fixed in the future release.
    console.log(await (await spectrometer.readProperty("serial number")).value())

    //call actions
    await spectrometer.invokeAction("connect")
    
    spectrometer.subscribeEvent("measurement_event", async(data) => {
        const value = await data.value()
        console.log("event : ", value)            
    }).then((subscription) => {
        console.debug("subscribed to intensity measurement event")
    })
    
    await spectrometer.invokeAction("start_acquisition")
})
