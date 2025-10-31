<table>
  <tr>
    <th>Protocol</th>
    <th>Plausible Use Cases</th>
    <th>Operations</th>
  </tr>
  <tr>
    <td>HTTP</td>
    <td>Web Apps</td>
    <td rowspan="4">
        <code>readproperty</code>, 
        <code>writeproperty</code>, 
        <code>observeproperty</code>, 
        <code>unobserveproperty</code>, 
        <code>invokeaction</code>, 
        <code>subscribeevent</code>,
        <code>unsubscribeevent</code>,
        <code>readmultipleproperties</code>,
        <code>writemultipleproperties</code>,
        <code>readallproperties</code>,
        <code>writeallproperties</code>
        <br>
        properties and actions can be operated in a oneway and no-block manner (issue and query later format) as well
    </td>
  </tr>
  <tr>
    <td>ZMQ TCP</td>
    <td>Networked Control Systems, subnet protected containerized apps like in Kubernetes</td>
  </tr>
  <tr>
    <td>ZMQ IPC</td>
    <td>Desktop Applications, Python Dashboards without exposing device API directly on network</td>
  </tr>
  <tr>
    <td>ZMQ INPROC</td>
    <td>
        High Speed Desktop Applications (again, not exposed on network), currently you will need some CPP magic or disable GIL to leverage it fully
    </td>
  </tr>
  <tr>
    <td>MQTT</td>
    <td>
        Reliable pub-sub & incorporating into existing systems that use MQTT for <br> lightweight messaging
    </td>
    <td>
        <code>observeproperty</code>, 
        <code>unobserveproperty</code>, 
        <code>subscribeevent</code>, 
        <code>unsubscribeevent</code>
    </td>
  </tr>
  <tr>
    <td>MQTT with websockets</td>
    <td>
        Reliable pub-sub for web applications, planned for November 2025 release.
    </td>
    <td>
        <code>observeproperty</code>, 
        <code>unobserveproperty</code>, 
        <code>subscribeevent</code>, 
        <code>unsubscribeevent</code>
    </td>
  </tr>
</table>
