# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class SupportPersonnel(models.Model):
	id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
	name = models.CharField(db_column='Name', max_length=63)  # Field name made lowercase.
	uid = models.CharField(db_column='UID', unique=True, max_length=31)  # Field name made lowercase.
	isActive = models.IntegerField(db_column='IsActive', default=1)  # Field name made lowercase.
	phoneNo = models.CharField(db_column='PhoneNo', unique=True, max_length=8)  # Field name made lowercase.
	email = models.EmailField(db_column='Email', unique=True, max_length=63)  # Field name made lowercase.
	
	def __str__(self):
		return self.name

	class Meta:
		managed = True
		db_table = 'supportpersonnel'


class Concern(models.Model):
	id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
	name = models.CharField(db_column='Name', max_length=31)  # Field name made lowercase.
	enabled = models.IntegerField(db_column='Enabled', default=1)  # Field name made lowercase.
	created_timestamp = models.DateTimeField(db_column='Created_Timestamp', auto_now_add=True)  # Field name made lowercase.
	z_index = models.IntegerField(db_column='Z_Index')  # Field name made lowercase.
	parent_id = models.ForeignKey('self', models.DO_NOTHING, db_column='Parent_Id', default=1, blank=True)  # Field name made lowercase.
	
	def __str__(self):
		return self.name
		
	def get_Parent_Name(self):
		return self.parent_id.name
		
	def has_child(self):
		return Concern.objects.filter(parent_id = self.id).count() > 0
	
	class Meta:
		managed = True
		db_table = 'concern'
		ordering = ['z_index']

class Issue(models.Model):
	id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
	issue_raised_timestamp = models.DateTimeField(db_column='Issue_Raised_Timestamp', auto_now_add=True)  # Field name made lowercase.
	workstation_id = models.IntegerField(db_column='Workstation_Id')  # Field name made lowercase.
	acked = models.IntegerField(db_column='Acked', default=0)  # Field name made lowercase.
	concern = models.ForeignKey(Concern, models.DO_NOTHING, db_column='Concern_Id')  # Field name made lowercase.

	class Meta:
		managed = True
		db_table = 'issue'


class Acknowledgement(models.Model):
	id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
	issue_acked_timestamp = models.DateTimeField(db_column='Issue_Acked_Timestamp', auto_now_add=True)  # Field name made lowercase.
	remarks = models.CharField(db_column='Remarks', max_length=511, blank=True, null=True)  # Field name made lowercase.
	issue = models.ForeignKey('Issue', models.DO_NOTHING, db_column='Issue_Id')  # Field name made lowercase.
	supportPersonnel = models.ForeignKey('SupportPersonnel', models.DO_NOTHING, db_column='SupportPersonnel_Id')  # Field name made lowercase.

	class Meta:
		managed = True
		db_table = 'acknowledgement'


class NotifyRelationship(models.Model):
	id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
	supportPersonnel = models.ForeignKey('SupportPersonnel', models.DO_NOTHING, db_column='SupportPersonnel_Id')  # Field name made lowercase.
	concern = models.ForeignKey(Concern, models.DO_NOTHING, db_column='Concern_Id')  # Field name made lowercase.
	
	class Meta:
		managed = True
		db_table = 'notifyrelationship'
		unique_together = (('supportPersonnel', 'concern'),)
