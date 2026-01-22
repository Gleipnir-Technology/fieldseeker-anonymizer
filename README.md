# Fieldseeker Anonymizer

A small Python program. This grew out of the need for realistic data to get through Apple App Store review of [Nidus](https://nidus.cloud).

First you'll need to create some CSV files from a `nidus-sync` database:

```
\copy fieldseeker.pointlocation TO './pointlocation-anonymized.csv' WITH (FORMAT csv, HEADER);
\copy fieldseeker.mosqitoinspection TO './mosqitoinspection-anonymized.csv' WITH (FORMAT csv, HEADER);
\copy fieldseeker.treatment TO './treatment-anonymized.csv' WITH (FORMAT csv, HEADER);
```

You'll need to figure out the orgnanization ID of your target organization. Mine is 3. Modify the command below to run the python program

```
python3 anonymize.py mosquitoinspection.csv pointlocation.csv treatment.csv -c creator editor fieldtech accessdesc assignedtech creator editor last_edited_user -s organization_id=<org_id> && cp *-anonymized.csv /tmp/
```

Then read in the resulting files

```
\copy fieldseeker.pointlocation FROM '/tmp/pointlocation-anonymized.csv' WITH (FORMAT csv, HEADER);
\copy fieldseeker.mosqitoinspection FROM '/tmp/mosqitoinspection-anonymized.csv' WITH (FORMAT csv, HEADER);
\copy fieldseeker.treatment FROM '/tmp/treatment-anonymized.csv' WITH (FORMAT csv, HEADER);
```

At this point you should have however many thousand new rows
