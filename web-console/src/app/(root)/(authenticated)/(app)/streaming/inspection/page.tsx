// Browse tables and views & insert data into tables.
'use client'

import { BreadcrumbsHeader } from '$lib/components/common/BreadcrumbsHeader'
import { ErrorOverlay } from '$lib/components/common/table/ErrorOverlay'
import { InsertionTable } from '$lib/components/streaming/import/InsertionTable'
import { InspectionTable } from '$lib/components/streaming/inspection/InspectionTable'
import { PipelineId } from '$lib/services/manager'
import { PipelineManagerQuery } from '$lib/services/pipelineManagerQuery'
import { Pipeline, PipelineStatus } from '$lib/types/pipeline'
import { useSearchParams } from 'next/navigation'
import { SyntheticEvent, useEffect, useState } from 'react'
import { ErrorBoundary } from 'react-error-boundary'

import TabContext from '@mui/lab/TabContext'
import TabList from '@mui/lab/TabList'
import TabPanel from '@mui/lab/TabPanel'
import { Alert, AlertTitle, Autocomplete, Box, FormControl, Link, MenuItem, TextField } from '@mui/material'
import Grid from '@mui/material/Grid'
import Tab from '@mui/material/Tab'
import { useQuery } from '@tanstack/react-query'

import type { Row } from '$lib/components/streaming/import/InsertionTable'
const TablesBreadcrumb = (props: { pipeline: Pipeline; relation: string; tables: string[]; views: string[] }) => {
  return (
    <Box sx={{ mb: '-1rem' }}>
      <FormControl sx={{ mt: '-1rem' }}>
        <Autocomplete
          size='small'
          options={props.tables
            .map(name => ({ type: 'Tables', name }))
            .concat(props.views.map(name => ({ type: 'Views', name })))}
          groupBy={option => option.type}
          getOptionLabel={o => o.name}
          sx={{ width: 400 }}
          renderInput={params => <TextField {...params} value={props.relation} label='Tables and Views' />}
          value={{ name: props.relation, type: '' }}
          renderOption={(_props, item) => (
            <MenuItem
              key={item.name}
              value={item.name}
              {...{
                component: Link,
                href: `?pipeline_id=${props.pipeline.descriptor.pipeline_id}&relation=${item.name}`
              }}
            >
              {item.name}
            </MenuItem>
          )}
        />
      </FormControl>
    </Box>
  )
}

const TableWithInsertTab = (props: {
  pipeline: Pipeline
  handleChange: ((event: SyntheticEvent<Element, Event>, value: any) => void) | undefined
  tab: string
  relation: string
}) => {
  const logError = (error: Error) => {
    console.error('InspectionTable error: ', error)
  }
  const [rows, setRows] = useState<Row[]>([])

  const { pipeline, handleChange, tab, relation } = props
  return (
    <TabContext value={tab}>
      <TabList centered variant='fullWidth' onChange={handleChange} aria-label='tabs to insert and browse relations'>
        <Tab value='browse' label={`Browse ${relation}`} />
        <Tab value='insert' label='Insert New Rows' />
      </TabList>
      <TabPanel value='browse'>
        <ViewDataTable pipeline={pipeline} relation={relation} />
      </TabPanel>
      <TabPanel value='insert'>
        {pipeline.state.current_status === PipelineStatus.RUNNING ? (
          <ErrorBoundary FallbackComponent={ErrorOverlay} onError={logError} key={location.pathname}>
            <InsertionTable pipeline={pipeline} name={relation} insert={{ rows, setRows }} />
          </ErrorBoundary>
        ) : (
          <Alert severity='info'>
            <AlertTitle>Pipeline not running</AlertTitle>
            Pipeline must be running to insert data. Try starting it.
          </Alert>
        )}
      </TabPanel>
    </TabContext>
  )
}

const ViewDataTable = (props: { pipeline: Pipeline; relation: string }) => {
  const { pipeline, relation } = props
  const logError = (error: Error) => {
    console.error('InspectionTable error: ', error)
  }

  return pipeline.state.current_status === PipelineStatus.RUNNING ||
    pipeline.state.current_status === PipelineStatus.PAUSED ? (
    <ErrorBoundary FallbackComponent={ErrorOverlay} onError={logError} key={location.pathname}>
      <InspectionTable pipeline={pipeline} name={relation} />
    </ErrorBoundary>
  ) : (
    <ErrorOverlay error={new Error(`'${pipeline.descriptor.name}' is not deployed.`)} />
  )
}

const IntrospectInputOutput = () => {
  const [pipelineId, setPipelineId] = useState<PipelineId | undefined>(undefined)
  const [relation, setRelation] = useState<string | undefined>(undefined)
  const [tab, setTab] = useState<'browse' | 'insert'>('browse')
  const [tables, setTables] = useState<string[] | undefined>(undefined)
  const [views, setViews] = useState<string[] | undefined>(undefined)

  const handleChange = (event: SyntheticEvent, newValue: 'browse' | 'insert') => {
    setTab(newValue)
  }

  // Parse config, view, tab arguments from router query
  const query = Object.fromEntries(useSearchParams().entries())
  useEffect(() => {
    const { pipeline_id, relation, tab } = query
    if (typeof tab === 'string' && (tab === 'browse' || tab === 'insert')) {
      setTab(tab)
    }
    if (typeof pipeline_id === 'string') {
      setPipelineId(pipeline_id)
    }
    if (typeof relation === 'string') {
      setRelation(relation)
    }
  }, [query, pipelineId, setPipelineId, setRelation])

  // Load the pipeline
  const [pipeline, setPipeline] = useState<Pipeline | undefined>(undefined)
  const configQuery = useQuery({
    ...PipelineManagerQuery.pipelineStatus(pipelineId!),
    enabled: pipelineId !== undefined
  })
  useEffect(() => {
    if (!configQuery.isPending && !configQuery.isError) {
      setPipeline(configQuery.data)
    }
  }, [configQuery.isPending, configQuery.isError, configQuery.data, setPipeline])

  // Load the last revision of the pipeline
  const pipelineRevisionQuery = useQuery({
    ...PipelineManagerQuery.pipelineLastRevision(pipelineId!),
    enabled: pipelineId !== undefined
  })
  useEffect(() => {
    if (!pipelineRevisionQuery.isPending && !pipelineRevisionQuery.isError) {
      const pipelineRevision = pipelineRevisionQuery.data
      const program = pipelineRevision?.program
      setTables(program?.schema?.inputs.map(v => v.name) || [])
      setViews(program?.schema?.outputs.map(v => v.name) || [])
    }
  }, [pipelineRevisionQuery.isPending, pipelineRevisionQuery.isError, pipelineRevisionQuery.data])

  // If we request to be on the insert tab for a view, we force-switch to the
  // browse tab.
  useEffect(() => {
    if (relation && views && views.includes(relation) && tab == 'insert') {
      setTab('browse')
    }
  }, [setTab, relation, views, tab])

  const relationValid =
    pipeline && relation && tables && views && (tables.includes(relation) || views.includes(relation))

  return pipelineId !== undefined &&
    !configQuery.isPending &&
    !configQuery.isError &&
    !pipelineRevisionQuery.isPending &&
    !pipelineRevisionQuery.isError &&
    relationValid ? (
    <>
      <BreadcrumbsHeader>
        <Link href={`/streaming/management`}>Pipelines</Link>
        <Link href={`/streaming/management/#${pipeline.descriptor.pipeline_id}`}>{pipeline.descriptor.name}</Link>
        <TablesBreadcrumb pipeline={pipeline} relation={relation} tables={tables} views={views}></TablesBreadcrumb>
      </BreadcrumbsHeader>
      <Grid item xs={12}>
        {tables.includes(relation) && (
          <TableWithInsertTab pipeline={pipeline} handleChange={handleChange} tab={tab} relation={relation} />
        )}
        {views.includes(relation) && <ViewDataTable pipeline={pipeline} relation={relation} />}
      </Grid>
    </>
  ) : (
    relation && tables && views && !(tables.includes(relation) || views.includes(relation)) && (
      <Alert severity='error'>
        <AlertTitle>Relation not found</AlertTitle>
        Unknown table or view: {relation}
      </Alert>
    )
  )
}

export default IntrospectInputOutput
