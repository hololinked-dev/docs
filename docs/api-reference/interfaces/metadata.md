# Metadata

Metadata generators are device APIs or device description languages. One can either create a Thing
in code and generate metadata (code-first), or create a Thing *from* a metadata (API-first). The interface 
required to do this is defined here. 

A specific metadata format is a bundle of five classes: one per core component - Property, Action, Event and a common base class for common metadata among them, and a class that puts them together.

See code of `hololinked.core.metadata.td` for a reference implementation for the W3C Web of Things. 

::: hololinked.core.interfaces.metadata.MetadataFormat
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - thing
            - property
            - action
            - event
            - interaction

::: hololinked.core.interfaces.metadata.Metadata
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - thing
            - generate
            - produce
            - add_interactions
            - skip_properties
            - skip_actions
            - skip_events
            - skip_names
            - ignore_errors
            - json

::: hololinked.core.interfaces.metadata.InteractionMetadata
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - what
            - name
            - objekt
            - owner
            - owner_cls
            - thing_cls
            - thing_id
            - build
            - build_non_compliant_metadata
            - from_descriptor
            - to_descriptor
            - from_metadata
            - override_defaults
            - register_descriptor
            - json

::: hololinked.core.interfaces.metadata.PropertyMetadata
    options:
        show_root_heading: true
        heading_level: 2

::: hololinked.core.interfaces.metadata.ActionMetadata
    options:
        show_root_heading: true
        heading_level: 2

::: hololinked.core.interfaces.metadata.EventMetadata
    options:
        show_root_heading: true
        heading_level: 2
