<table>
  <tr>
    <th>Protocol</th>
    <th>Plausible Use Cases</th>
    <th>Operations</th>
    <th>Security</th>
  </tr>
  <tr>
    <td>HTTP</td>
    <td>Web Apps</td>
    <td rowspan="4">
      <code>readproperty</code>, <br/>
      <code>writeproperty</code>, <br/>
      <code>observeproperty</code>, <br/>
      <code>unobserveproperty</code>, <br/>
      <code>invokeaction</code>, <br/>
      <code>subscribeevent</code>, <br/>
      <code>unsubscribeevent</code>, <br/>
      <code>readmultipleproperties</code>, <br/>
      <code>writemultipleproperties</code>, <br/>
      <code>readallproperties</code>, <br/>
      <code>writeallproperties</code> <br/>
      properties and actions can be operated in a oneway and no-block manner (issue and query later format) as well
    </td>
    <td>
      username-password, <br/>
      device API key, <br/>
      IP filter, <br/>
      OAuth2 OIDC (experimental)
    </td>
  </tr>
  <tr>
    <td>ZMQ TCP</td>
    <td>Networked Control Systems, subnet protected containerized apps like in Kubernetes</td>
    <td>
      username-password planned, <br/>
      device API key planned
    </td>
  </tr>
  <tr>
    <td>ZMQ IPC</td>
    <td>Desktop Applications, Python Dashboards without exposing device API directly on network</td>
    <td>
      username-password planned, <br/>
      device API key planned
    </td>
  </tr>
  <tr>
    <td>ZMQ INPROC</td>
    <td>
      High Speed Desktop Applications (again, not exposed on network), currently you will need some CPP magic or disable GIL to leverage it fully
    </td>
    <td>
      No security, meant for in-process communication only
    </td>
  </tr>
  <tr>
    <td>MQTT</td>
    <td>
      Reliable pub-sub & incorporating into existing systems that use MQTT for <br> lightweight messaging
    </td>
    <td>
      <code>observeproperty</code>, <br/>
      <code>unobserveproperty</code>, <br/>
      <code>subscribeevent</code>, <br/>
      <code>unsubscribeevent</code>
    </td>
    <td>
      username-password, <br/>
      TLS with client certificates (you set this up in the broker anyway)
    </td>
  </tr>
  <tr>
    <td>MQTT with websockets</td>
    <td>
      Reliable pub-sub for web applications, planned for March 2026 release.
    </td>
    <td>
      <code>observeproperty</code>, <br/>
      <code>unobserveproperty</code>, <br/>
      <code>subscribeevent</code>, <br/>
      <code>unsubscribeevent</code>
    </td>
    <td>
      username-password, <br/>
      TLS with client certificates (you set this up in the broker anyway)
    </td>
  </tr>
</table>
